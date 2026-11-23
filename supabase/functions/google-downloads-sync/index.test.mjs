import assert from 'node:assert/strict';
import {registerHooks} from 'node:module';
import test from 'node:test';

const moduleUrl = source => `data:text/javascript,${encodeURIComponent(source)}`;
const observationTime = '2026-11-23T00:57:55.086815+00:00';
const app = (packageId, status = 'production', name = packageId) => ({name, packageId, status});

function registryRow(apps, overrides = {}) {
  return {status: 'verified', detail: JSON.stringify({
    schemaVersion: 1, kind: 'release_status_observation', platform: 'google', observedAt: observationTime,
    counts: {
      registered: apps.length,
      ...Object.fromEntries(['production', 'internal', 'draft'].map(status => [
        status, apps.filter(entry => entry.status === status).length,
      ])),
    },
    apps, ...overrides,
  })};
}

async function invokeCollector(t, {previousApps = [], registry = null, registryError = null, report}) {
  const previous = {apps: previousApps};
  const reads = [];
  const writes = [];
  const reportPaths = [];
  const oauthRequests = [];
  const defaultReport = () => new Response('fixture-private-response', {status: 403});
  const env = {
    GOOGLE_DOWNLOADS_CRON_SECRET: 'fixture-cron',
    GOOGLE_PLAY_SERVICE_ACCOUNT_JSON: JSON.stringify({
      client_email: 'fixture@example.invalid', private_key: 'fixture-key',
    }),
    GOOGLE_PLAY_REPORT_BUCKET: 'pubsite_prod_rev_fixture',
  };
  const db = {
    from(table) {
      assert.equal(table, 'admin_app_sync_runtime');
      return {
        select(column) {
          return {
            eq(key, value) {
              assert.equal(key, 'id');
              reads.push([value, column]);
              if (value === 'google_release_status') {
                return {single: async () => ({data: registry, error: registryError})};
              }
              assert.equal(value, 'google_downloads');
              return {single: async () => ({data: {detail: JSON.stringify(previous)}})};
            },
          };
        },
        async upsert(row) { writes.push(row); return {error: null}; },
      };
    },
  };
  let handler;
  globalThis.Deno = {
    env: {get: name => env[name]},
    serve: callback => { handler = callback; },
    createClient: () => db,
  };
  t.after(() => { delete globalThis.Deno; });

  t.mock.method(Date, 'now', () => Date.parse('2026-11-23T06:00:00Z'));
  t.mock.method(globalThis, 'fetch', async (url, options) => {
    if (url === 'https://oauth2.googleapis.com/token') {
      oauthRequests.push(url);
      return Response.json({access_token: 'fixture-token'});
    }
    assert.equal(options.headers.Authorization, 'Bearer fixture-token');
    const path = decodeURIComponent(new URL(url).pathname).split('/').at(-1);
    reportPaths.push(path);
    return (report ?? defaultReport)(path);
  });

  const substitutes = new Map([
    ['https://esm.sh/@supabase/supabase-js@2.116.0', moduleUrl('export const createClient = (...args) => Deno.createClient(...args);')],
    ['npm:jose@5.9.6', moduleUrl(`
      export const importPKCS8 = async () => ({});
      export class SignJWT {
        setProtectedHeader() { return this; }
        setIssuer() { return this; }
        setAudience() { return this; }
        setIssuedAt() { return this; }
        setExpirationTime() { return this; }
        async sign() { return 'fixture-assertion'; }
      }
    `)],
  ]);
  const hooks = registerHooks({
    resolve(specifier, context, nextResolve) {
      return nextResolve(substitutes.get(specifier) ?? specifier, context);
    },
  });
  t.after(() => hooks.deregister());

  await import(`./index.ts?fixture=${encodeURIComponent(t.name)}`);
  const response = await handler(new Request('https://example.invalid/collector', {
    method: 'POST', headers: {'x-sync-secret': 'fixture-cron'},
  }));
  const body = await response.json();
  return {response, body, reads, writes, reportPaths, oauthRequests};
}

const fold = app('com.apholdings.foldblock', 'production', '폴드블록');
const hotel = app('com.hotelranker', 'production', '호텔랭커');
const quiz = app('com.quizarena', 'internal', '퀴즈랭커');
const dad = app('com.apholdings.dadandme', 'draft', '아빠랑 나랑');
const staleApps = [
  {...fold, status: 'not_created', installs: 31}, {...hotel, installs: 42},
  {...dad, packageId: 'com.apholdings.seunggyuandme', installs: 51},
];
const registryRead = [['google_release_status', 'status,detail']];

test('persists failed report package IDs only for verified production apps on the diagnostic list', async t => {
  const known = app('com.apholdings.dawngrace');
  const unlisted = app('com.apholdings.fixtureunregistered');
  const apps = [known, unlisted, hotel, quiz, dad];
  const {response, body, reads, writes, reportPaths} = await invokeCollector(t, {
    previousApps: apps, registry: registryRow(apps),
  });

  assert.deepEqual(reportPaths, [
    'installs_com.apholdings.dawngrace_202610_country.csv',
    'installs_com.apholdings.fixtureunregistered_202610_country.csv',
    'installs_com.hotelranker_202610_country.csv',
    'installs_com.quizarena_202610_country.csv',
    'installs_com.apholdings.dadandme_202610_country.csv',
  ]);
  assert.equal(response.status, 200);
  assert.equal(body.status, 'source_error');
  assert.equal(body.failedApps, 5);
  assert.equal(Object.hasOwn(body, 'failures'), false);
  assert.deepEqual(writes.map(row => [row.id, row.status]), [['google_downloads_sync', 'source_error']]);

  const detail = JSON.parse(writes[0].detail);
  const failure = {month: '202610', stage: 'http', code: 'permission_required', httpStatus: 403};
  assert.equal(detail.failedApps, 5);
  assert.deepEqual(detail.failures, [
    {packageId: known.packageId, ...failure}, failure, {packageId: hotel.packageId, ...failure}, failure, failure,
  ]);
  assert.deepEqual(reads, registryRead);
});

const noReport = () => new Response(null, {status: 404});

function csvReport(packageId, date, count) {
  return new Response(`Date,Package name,Country,Daily Device Installs,Daily User Installs\n${date},${packageId},KR,999,${count}\n`);
}

test('uses verified release IDs and persists the documented November CSV including a reported zero', async t => {
  const {body, reads, writes, reportPaths} = await invokeCollector(t, {
    previousApps: staleApps,
    registry: registryRow([fold, hotel, quiz, dad]),
    report(path) {
      if (path === 'installs_com.hotelranker_202611_country.csv') return csvReport(hotel.packageId, '2026-11-03', 4);
      if (path === 'installs_com.apholdings.foldblock_202611_country.csv') return csvReport(fold.packageId, '2026-11-04', 0);
      return noReport();
    },
  });

  assert.equal(body.status, 'collected');
  assert.deepEqual(reads, registryRead);
  assert.deepEqual(reportPaths, [
    'installs_com.apholdings.foldblock_202610_country.csv', 'installs_com.apholdings.foldblock_202611_country.csv',
    'installs_com.hotelranker_202610_country.csv', 'installs_com.hotelranker_202611_country.csv',
    'installs_com.quizarena_202610_country.csv', 'installs_com.quizarena_202611_country.csv',
    'installs_com.apholdings.dadandme_202610_country.csv', 'installs_com.apholdings.dadandme_202611_country.csv',
  ]);
  assert.deepEqual(writes.map(row => [row.id, row.status]), [
    ['google_downloads', 'ok'], ['google_downloads_sync', 'collected'],
  ]);
  const snapshot = JSON.parse(writes[0].detail);
  assert.deepEqual([snapshot.periodStart, snapshot.periodEnd], ['2026-10-27', '2026-11-23']);
  assert.deepEqual(snapshot.apps, [
    {...fold, installs: 0, reportedDays: 1, lastReportDay: '2026-11-04', complete: false,
      metric: 'installed_users', sourceStatus: 'partial_report'},
    {...hotel, installs: 4, reportedDays: 1, lastReportDay: '2026-11-03', complete: false,
      metric: 'installed_users', sourceStatus: 'partial_report'},
    {...quiz, installs: null, reportedDays: 0, lastReportDay: null, complete: false,
      metric: 'installed_users', sourceStatus: 'waiting_report'},
    {...dad, installs: null, reportedDays: 0, lastReportDay: null, complete: false,
      metric: 'installed_users', sourceStatus: 'waiting_report'},
  ]);
});

test('keeps the previous snapshot if the reports have no in-period rows', async t => {
  const registry = registryRow([hotel, fold], {observedAt: '2024-02-29T23:59:59.123456+09:00'});
  registry.detail = JSON.parse(registry.detail);
  const {body, writes} = await invokeCollector(t, {
    previousApps: staleApps, registry,
    report(path) {
      if (path === 'installs_com.hotelranker_202610_country.csv') return csvReport(hotel.packageId, '2026-10-01', 30);
      if (path === 'installs_com.apholdings.foldblock_202611_country.csv') {
        return new Response('Date,Package name,Country,Daily User Installs');
      }
      return noReport();
    },
  });

  assert.equal(body.status, 'waiting_report');
  assert.deepEqual(writes.map(row => [row.id, row.status]), [['google_downloads_sync', 'waiting_report']]);
});

test('can write an official snapshot without a previous snapshot registry', async t => {
  const {body, reads, writes} = await invokeCollector(t, {
    registry: registryRow([hotel]),
    report: path => path.includes('202611') ? csvReport(hotel.packageId, '2026-11-03', 7) : noReport(),
  });

  assert.equal(body.status, 'collected');
  assert.deepEqual(reads, registryRead);
  assert.equal(JSON.parse(writes[0].detail).apps[0].installs, 7);
});

for (const [scenario, registry, registryError, diagnostic] of [
  ['missing row', null, null, 'registry_missing'],
  ['registry read fails', null, {message: 'fixture-private-query-detail'}, 'registry_read'],
  ['unverified status', {...registryRow([hotel]), status: 'pending'}, null, 'registry_invalid'],
  ['malformed JSON', {status: 'verified', detail: '{'}, null, 'registry_invalid'],
  ['empty roster', registryRow([]), null, 'registry_invalid'],
  ['wrong platform', registryRow([hotel], {platform: 'apple'}), null, 'registry_invalid'],
  ['invalid timestamp', registryRow([hotel], {observedAt: '2026'}), null, 'registry_invalid'],
  ['impossible calendar date', registryRow([hotel], {observedAt: '2026-02-30T00:00:00.000000+00:00'}), null,
    'registry_invalid'],
  ['invalid observation clock', registryRow([hotel], {observedAt: '2026-11-23T24:00:00.000000+00:00'}), null,
    'registry_invalid'],
  ['invalid observation offset', registryRow([hotel], {observedAt: '2026-11-23T00:00:00.000000+00:60'}), null,
    'registry_invalid'],
  ['incoherent counts', registryRow([hotel], {counts: {registered: 2, production: 1, internal: 0, draft: 0}}), null,
    'registry_invalid'],
  ['duplicate package', registryRow([hotel, hotel]), null, 'registry_invalid'],
  ['unsupported release state', registryRow([app('com.apholdings.bad', 'not_created')]), null, 'registry_invalid'],
  ['malformed package', registryRow([app('com.invalid/name')]), null, 'registry_invalid'],
  ['object package', registryRow([app({unexpected: 'fixture-private-registry-value'}, 'production', 'Bad')]), null,
    'registry_invalid'],
]) {
  test(`preserves the previous snapshot without querying Google for ${scenario}`, async t => {
    const {body, reads, writes, reportPaths, oauthRequests} = await invokeCollector(t, {
      previousApps: staleApps, registry, registryError,
    });

    assert.equal(body.status, 'connection_error');
    assert.equal(body.diagnostic, diagnostic);
    assert.deepEqual(reads, registryRead);
    assert.deepEqual(oauthRequests, []);
    assert.deepEqual(reportPaths, []);
    assert.deepEqual(writes.map(row => [row.id, row.status]), [['google_downloads_sync', 'connection_error']]);
    const storedDetail = JSON.parse(writes[0].detail);
    assert.equal(storedDetail.diagnostic, diagnostic);
    assert.equal(Object.hasOwn(storedDetail, 'failures'), false);
  });
}
