import assert from 'node:assert/strict';
import test from 'node:test';
import {aggregateInstalls, readInstallReport} from './core.mjs';

const bucket = 'pubsite_prod_rev_test-bucket';
const packageId = 'kr.example.fixture';
const month = '202611';
const header = 'Date,Package Name,Country,Daily Device Installs,Daily User Installs';

test('reads a UTF-16LE country report from the existing encoded Google Storage path', async () => {
  const csv = `${header}\r\n2026-11-01,${packageId},KR,999,12\r\n2026-11-02,${packageId},KR,999,0\r\n`;
  const response = new Response(Buffer.from(`\uFEFF${csv}`, 'utf16le'));
  const paths = [];
  const result = await readInstallReport(async path => {
    paths.push(path);
    return response;
  }, bucket, packageId, month);

  assert.deepEqual(paths, [
    'https://storage.googleapis.com/storage/v1/b/pubsite_prod_rev_test-bucket/o/stats%2Finstalls%2Finstalls_kr.example.fixture_202611_country.csv?alt=media',
  ]);
  assert.deepEqual(result, {
    rows: [
      {date: '2026-11-01', country: 'KR', count: 12},
      {date: '2026-11-02', country: 'KR', count: 0},
    ],
    missing: false,
    diagnostic: null,
  });
  assert.deepEqual(aggregateInstalls(result.rows, '2026-11-01', '2026-11-02'), {
    installs: 12,
    reportedDays: 2,
    lastReportDay: '2026-11-02',
    complete: true,
  });
});

test('accepts the documented Package name header and reads Daily User Installs', async () => {
  const csv = `${header.replace('Package Name', 'Package name')}\r\n2026-11-03,${packageId},KR,999,4\r\n`;
  const result = await readInstallReport(async () => new Response(Buffer.from(`\uFEFF${csv}`, 'utf16le')),
    bucket, packageId, month);

  assert.deepEqual(result, {rows: [{date: '2026-11-03', country: 'KR', count: 4}], missing: false, diagnostic: null});
});

for (const packageColumns of ['Package Name,Package name', 'Package name,Package name', 'Package Name,Package Name']) {
  test(`rejects ambiguous package columns ${packageColumns}`, async () => {
    const csv = `Date,${packageColumns},Country,Daily User Installs\n2026-11-03,${packageId},${packageId},KR,4\n`;
    const result = await readInstallReport(async () => new Response(csv), bucket, packageId, month);

    assert.deepEqual(result, {
      rows: [], missing: false,
      diagnostic: {
        packageId, month, stage: 'header', code: 'invalid_report',
        headers: ['Date', ...packageColumns.split(','), 'Country', 'Daily User Installs'],
      },
    });
  });
}

test('rejects an unauthorized package header spelling', async () => {
  const csv = 'Date,package name,Country,Daily User Installs';
  const {diagnostic} = await readInstallReport(async () => new Response(csv), bucket, packageId, month);

  assert.deepEqual(diagnostic, {
    packageId, month, stage: 'header', code: 'invalid_report', headers: ['Date', 'Country', 'Daily User Installs'],
  });
});

test('rejects a mismatched package value under the documented alias', async () => {
  const csv = 'Date,Package name,Country,Daily User Installs\n2026-11-03,kr.example.another,KR,4\n';
  const result = await readInstallReport(async () => new Response(csv), bucket, packageId, month);

  assert.deepEqual(result, {
    rows: [], missing: false, diagnostic: {packageId, month, stage: 'row', code: 'invalid_report'},
  });
});

test('requires Daily User Installs even when the documented package alias is present', async () => {
  const csv = `Date,Package name,Country,Daily Device Installs\n2026-11-03,${packageId},KR,4\n`;
  const result = await readInstallReport(async () => new Response(csv), bucket, packageId, month);

  assert.deepEqual(result, {
    rows: [], missing: false,
    diagnostic: {
      packageId, month, stage: 'header', code: 'invalid_report',
      headers: ['Date', 'Package name', 'Country', 'Daily Device Installs'],
    },
  });
  assert.equal(aggregateInstalls(result.rows, '2026-11-03', '2026-11-03').installs, null);
});

test('treats HTTP 404 as a missing report with unknown installs', async () => {
  const response = new Response('private response fixture', {status: 404});
  const result = await readInstallReport(async () => response, bucket, packageId, month);

  assert.deepEqual(result, {rows: [], missing: true, diagnostic: null});
  assert.equal(response.bodyUsed, false);
  assert.deepEqual(aggregateInstalls(result.rows, '2026-11-01', '2026-11-02'), {
    installs: null,
    reportedDays: 0,
    lastReportDay: null,
    complete: false,
  });
});

for (const [status, code] of [[403, 'permission_required'], [500, 'source_error']]) {
  test(`maps HTTP ${status} to ${code} without reading the error body`, async () => {
    const response = new Response('Bearer fixture-token\nprivate CSV body', {status});
    const result = await readInstallReport(async () => response, bucket, packageId, month);

    assert.deepEqual(result, {
      rows: [],
      missing: false,
      diagnostic: {packageId, month, stage: 'http', code, httpStatus: status},
    });
    assert.equal(response.bodyUsed, false);
  });
}

test('reports at most twenty recognized header names on schema failure', async () => {
  const malformedHeader = [
    'Date', 'Package Name', 'Daily Device Installs', 'Bearer fixture-token',
    'https://example.invalid/signed?token=private', 'customer_112233', 'A'.repeat(120),
    ...Array(21).fill('Country'),
  ].join(',');
  const response = new Response(`${malformedHeader}\n2026-11-01,${packageId},private-row,8\n`);
  const result = await readInstallReport(async () => response, bucket, packageId, month);

  assert.deepEqual(result, {
    rows: [],
    missing: false,
    diagnostic: {
      packageId, month, stage: 'header', code: 'invalid_report',
      headers: ['Date', 'Package Name', 'Daily Device Installs', ...Array(17).fill('Country')],
    },
  });
  assert.ok(result.diagnostic.headers.every(name => name.length <= 100));
});

test('reports a malformed row without emitting report data or partial results', async () => {
  const response = new Response(
    `${header}\n2026-11-01,${packageId},KR,999,12\n2026-11-02,${packageId},private-row,999,fixture-token\n`,
  );
  const result = await readInstallReport(async () => response, bucket, packageId, month);

  assert.deepEqual(result, {
    rows: [], missing: false, diagnostic: {packageId, month, stage: 'row', code: 'invalid_report'},
  });
});

test('reports malformed CSV quoting without emitting a partial header or body', async () => {
  const response = new Response(`${header}\n2026-11-01,${packageId},"private-row`);
  const result = await readInstallReport(async () => response, bucket, packageId, month);

  assert.deepEqual(result, {
    rows: [], missing: false, diagnostic: {packageId, month, stage: 'parse', code: 'invalid_report'},
  });
});

test('reports invalid encoding as decode failure', async () => {
  const response = new Response(Uint8Array.of(0xc0, 0xaf));
  const result = await readInstallReport(async () => response, bucket, packageId, month);

  assert.deepEqual(result, {
    rows: [], missing: false, diagnostic: {packageId, month, stage: 'decode', code: 'invalid_report'},
  });
});

test('reports a rejected fetch without copying its exception message', async () => {
  const result = await readInstallReport(async () => {
    throw new Error('Authorization: Bearer fixture-token at https://example.invalid/private');
  }, bucket, packageId, month);

  assert.deepEqual(result, {
    rows: [], missing: false, diagnostic: {packageId, month, stage: 'fetch', code: 'fetch_error'},
  });
});
