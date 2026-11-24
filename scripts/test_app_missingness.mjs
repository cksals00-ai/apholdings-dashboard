import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {metricSummary} from '../admin/app-finance.mjs';
const source=fs.readFileSync(new URL('../admin/admin.js',import.meta.url),'utf8');
const elements={};const ctx={apps:[{id:'a',name:'Known',status:'live'},{id:'b',name:'Unknown',status:'live'}],appMetrics:[{app_id:'a',day:'2026-10-27',downloads:0,units:0,iap_units:0,proceeds_krw:0}],appRuntime:[],VIZ_COUNTRY:[['KR','한국'],['FR','프랑스'],['US','미국'],['ETC','기타']],metricSummary,vizMetrics30:()=>ctx.appMetrics,appName:id=>id==='a'?'Known':'Unknown',vizEsc:String,vizWon:String,vizTip:(a,b)=>`title="${a} ${b}"`,kstToday:()=> '2026-10-28',vizAddDays:(s,n)=>{let d=new Date(s);d.setUTCDate(d.getUTCDate()+n);return d.toISOString().slice(0,10)},vizMD:String,$:id=>elements[id]??=( {})};
vm.createContext(ctx);
for(const name of ['renderAppBars','renderAppDaily']){const start=source.indexOf('function '+name+'('),end=source.indexOf('\nfunction ',start+10);vm.runInContext(source.slice(start,end),ctx);ctx[name]();}
assert.match(elements['#app-bars'].innerHTML,/Unknown[\s\S]*미수집/);
assert.match(elements['#app-daily'].innerHTML,/미수집/);
assert.match(elements['#app-daily'].innerHTML,/다운로드 0건/);
console.log('actual chart missingness checks passed');
