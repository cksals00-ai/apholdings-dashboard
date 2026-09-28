import assert from 'node:assert/strict';
import fs from 'node:fs';
import {calculatePlan} from '../admin/business-plan-model.mjs';

const assumptions={initialClients:0,cashBuffer:1000,recurringCostRate:.1,projectCostRate:.2,contentCostRate:.3,appCostRate:.1,platformFeeRate:.3,refundRate:.05,taxReserveRate:.2,serviceSameMonthReceipt:.5,appSettlementMonths:2,depreciationMonths:36,appPriceExVAT:100,paidConversionRate:.02,projectHours:10,contentHours:4,recurringHours:1,staffDeliveryHours:100,valuationMultipleLow:3,valuationMultipleHigh:5};
const stage={year:2027,startMonth:1,months:12,endClients:12,arpu:100,projectsPerMonth:1,projectPrice:1000,contentPerMonth:1,contentPrice:500,paidOrdersPerMonth:10,founderPayMonthly:100,staffFte:0,loadedStaffAnnual:12000,overheadMonthly:100,marketingMonthly:50,capex:360,founderDeliveryHours:40};
const fixture={schemaVersion:1,actuals:{openingCashKRW:null,interestBearingDebtKRW:null},assumptions,scenarios:{base:{monthlyChurn:.02,prospectCloseRate:.1,stages:[stage]}}};
const near=(a,b)=>assert.ok(Math.abs(a-b)<.00001,`${a} != ${b}`);
const first=calculatePlan(fixture);
assert.equal(first.months.length,12);near(first.years[0].clients,12);
near(first.months[0].appRevenue,950);near(first.months[0].platformFees,285);
near(first.months[0].depreciation,10);
near(first.months[0].cashReceipts,first.months[0].recurringRevenue+750);
near(first.months[1].cashReceipts,first.months[1].recurringRevenue+1500);
near(first.months[2].cashReceipts,first.months[2].recurringRevenue+1500+665);
near(first.months[0].receivables,750+665);
near(first.months[1].receivables,750+665*2);
assert.equal(first.additionalFundingRequired,null);assert.equal(first.endingCash,null);
assert.ok(first.maxReconciliationError<.00001);
for(const m of first.months){near(m.revenue-m.operatingExpenses-m.depreciation,m.operatingProfit);near(m.operatingCashFlow-m.capex,m.freeCashFlow);near(m.netProfit+m.depreciation-m.deltaAR,m.operatingCashFlow);}
const noLag=structuredClone(fixture);noLag.assumptions.appSettlementMonths=0;noLag.scenarios.base.monthlyChurn=0;
near(calculatePlan(noLag).months[0].cashReceipts,50+750+665);near(calculatePlan(noLag).months[0].receivables,750);
const withCash=structuredClone(fixture);withCash.actuals.openingCashKRW=2000;
assert.equal(calculatePlan(withCash).additionalFundingRequired,0);
const loss=structuredClone(fixture);loss.scenarios.base.stages[0].founderPayMonthly=100000;
assert.equal(calculatePlan(loss).valuationLow,0);assert.equal(calculatePlan(loss).years[0].taxReserve,0);
for(const [field,value] of [['platformFeeRate',2],['taxReserveRate',-1],['appSettlementMonths',1.5]]){const bad=structuredClone(fixture);bad.assumptions[field]=value;assert.throws(()=>calculatePlan(bad));}
const badPeriod=structuredClone(fixture);badPeriod.scenarios.base.stages.push({...stage,year:2029});assert.throws(()=>calculatePlan(badPeriod));
const before=JSON.stringify(fixture);calculatePlan(fixture);assert.equal(JSON.stringify(fixture),before);

// Optional private input stays outside the public repository and test output.
if(process.argv[2]){
  const plan=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
  for(const key of Object.keys(plan.scenarios)){
    const model=calculatePlan(plan,key);
    assert.equal(model.months.length,63);assert.equal(model.years.length,6);
    assert.deepEqual(model.years.filter(y=>y.months===12).map(y=>y.year),[2027,2028,2029,2030,2031]);
    for(const s of plan.scenarios[key].stages)near(model.months.find(m=>m.year===s.year&&m.month===s.startMonth+s.months-1).clients,s.endClients);
    assert.ok(model.maxReconciliationError<.01);
    assert.ok(model.months.every(m=>m.capacityGap===0));
    near(model.months.at(-1).cumulativeCash,model.years.reduce((a,y)=>a+y.freeCashFlow,0));
  }
}
console.log('PASS: monthly revenue, settlement lags, receivables, cash bridge, tax, valuation, capacity, targets and invalid inputs');
