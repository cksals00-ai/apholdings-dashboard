export function decodeReport(bytes){return new TextDecoder(bytes[0]===255&&bytes[1]===254?'utf-16le':bytes[0]===254&&bytes[1]===255?'utf-16be':'utf-8',{fatal:true}).decode(bytes);}
function csvRows(text){const rows=[];let row=[],field='',quoted=false;for(let i=0;i<text.length;i++){const c=text[i];if(c==='"'){if(quoted&&text[i+1]==='"'){field+='"';i++;}else quoted=!quoted;}else if(!quoted&&(c===','||c==='\n'||c==='\r')){row.push(field);field='';if(c!==','){if(c==='\r'&&text[i+1]==='\n')i++;if(row.some(v=>v!==''))rows.push(row);row=[];}}else field+=c;}if(quoted)throw Error('invalid_csv');row.push(field);if(row.some(v=>v!==''))rows.push(row);return rows;}
export const validDate=s=>/^\d{4}-\d{2}-\d{2}$/.test(s)&&Number.isFinite(Date.parse(s))&&new Date(s).toISOString().slice(0,10)===s;
const installColumns = ['Date', 'Country', 'Daily User Installs'];
const packageColumns = ['Package Name', 'Package name'];
const isPackageColumn = name => packageColumns.includes(name);
export function parseInstallCsv(text,pkg,onInvalidHeader) {
  const [header,...rows] = csvRows(text.replace(/^\uFEFF/,''));
  const [dateIndex, countryIndex, countIndex] = installColumns.map(name => header?.indexOf(name) ?? -1);
  const packageIndex = header?.findIndex(isPackageColumn) ?? -1;
  if ([dateIndex, countryIndex, countIndex, packageIndex].includes(-1) || packageIndex !== header.findLastIndex(isPackageColumn)) {
    onInvalidHeader?.(header);
    throw Error('schema');
  }
  return rows.map(row => {
    const date = row[dateIndex];
    const country = row[countryIndex];
    const count = row[countIndex];
    if (row[packageIndex] !== pkg || !validDate(date) || !country || !/^\d+$/.test(count) || !Number.isSafeInteger(Number(count))) {
      throw Error('invalid_row');
    }
    return {date, country, count: Number(count)};
  });
}
export function aggregateInstalls(rows,start,end){if(!validDate(start)||!validDate(end)||start>end)throw Error('period');const unique=new Map();for(const r of rows){if(r.date<start||r.date>end)continue;const k=r.date+'|'+r.country;if(unique.has(k)&&unique.get(k).count!==r.count)throw Error('conflicting_duplicate');unique.set(k,r);}const selected=[...unique.values()],days=new Set(selected.map(r=>r.date));const expected=(Date.parse(end)-Date.parse(start))/86400000+1;const sum=selected.reduce((s,r)=>s+r.count,0);if(!Number.isSafeInteger(sum))throw Error('overflow');return {installs:selected.length?sum:null,reportedDays:days.size,lastReportDay:[...days].sort().at(-1)||null,complete:days.size===expected};}

// An invalid first record may contain arbitrary data. Emit only known column names.
const diagnosticHeaderNames = new Set([
  ...installColumns, ...packageColumns,
  'Daily Device Installs', 'Daily Device Uninstalls', 'Daily User Uninstalls',
  'Active Device Installs', 'Total User Installs',
]);

/**
 * @param {(path: string) => Promise<Response>} fetchReport
 * @param {string} bucket
 * @param {string} packageId
 * @param {string} month
 */
export async function readInstallReport(fetchReport, bucket, packageId, month) {
  const failure = (stage, code, details = {}) => ({
    rows: [], missing: false, diagnostic: {packageId, month, stage, code, ...details},
  });
  const object = `stats/installs/installs_${packageId}_${month}_country.csv`;
  const path = `https://storage.googleapis.com/storage/v1/b/${encodeURIComponent(bucket)}/o/${encodeURIComponent(object)}?alt=media`;
  let response;
  try {
    response = await fetchReport(path);
  } catch {
    return failure('fetch', 'fetch_error');
  }

  if (response.status === 404) return {rows: [], missing: true, diagnostic: null};
  if (!response.ok) {
    const code = response.status === 403 ? 'permission_required' : 'source_error';
    return failure('http', code, {httpStatus: response.status});
  }

  let text;
  try {
    text = decodeReport(new Uint8Array(await response.arrayBuffer()));
  } catch {
    return failure('decode', 'invalid_report');
  }

  let headers;
  try {
    const rows = parseInstallCsv(text, packageId, header => {
      headers = [];
      for (const name of header ?? []) {
        if (name.length <= 100 && diagnosticHeaderNames.has(name)) headers.push(name);
        if (headers.length === 20) break;
      }
    });
    return {rows, missing: false, diagnostic: null};
  } catch (error) {
    if (headers) return failure('header', 'invalid_report', {headers});
    const stage = error instanceof Error && error.message === 'invalid_row' ? 'row' : 'parse';
    return failure(stage, 'invalid_report');
  }
}
