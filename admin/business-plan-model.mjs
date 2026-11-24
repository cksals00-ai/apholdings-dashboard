// Pure management-planning model. No business-specific figures or credentials.
// KRW, calendar months, VAT-exclusive revenue. Fractional clients are forecasts.
export const MODEL_VERSION = '1.0.0';

const finite = (v, name, min = 0, max = Infinity) => {
  if (!Number.isFinite(v) || v < min || v > max) throw new Error(`Invalid ${name}`);
  return v;
};

export function calculatePlan(plan, scenarioKey = 'base') {
  if (plan.schemaVersion !== 1) throw new Error('Unsupported plan version');
  const p = plan.assumptions;
  const scenario = plan.scenarios[scenarioKey];
  if (!p || !scenario?.stages?.length) throw new Error('Missing assumptions');
  for (const key of ['recurringCostRate','projectCostRate','contentCostRate','appCostRate','platformFeeRate','refundRate','taxReserveRate','serviceSameMonthReceipt','paidConversionRate']) finite(p[key], key, 0, 1);
  for (const key of ['initialClients','cashBuffer','appPriceExVAT','projectHours','contentHours','recurringHours','staffDeliveryHours']) finite(p[key], key);
  finite(p.depreciationMonths, 'depreciationMonths', 1);
  finite(p.valuationMultipleLow, 'valuationMultipleLow');
  finite(p.valuationMultipleHigh, 'valuationMultipleHigh', p.valuationMultipleLow);
  finite(p.paidConversionRate, 'paidConversionRate', .00001, 1);
  finite(p.appSettlementMonths, 'appSettlementMonths', 0, 12);
  if (!Number.isInteger(p.appSettlementMonths)) throw new Error('Invalid settlement lag');
  const churn = finite(scenario.monthlyChurn, 'churn', 0, .99);
  const closeRate = finite(scenario.prospectCloseRate, 'close rate', .00001, 1);
  let clients = p.initialClients, cumulativeCash = 0, previousAR = 0;
  let previousServices = 0, index = 0;
  const months = [], capexLots = [], appNetHistory = [];
  for (const stage of scenario.stages) {
    for (const key of ['year','startMonth','months','endClients','arpu','projectsPerMonth','projectPrice','contentPerMonth','contentPrice','paidOrdersPerMonth','founderPayMonthly','staffFte','loadedStaffAnnual','overheadMonthly','marketingMonthly','capex','founderDeliveryHours']) finite(stage[key], key);
    if (!Number.isInteger(stage.year) || !Number.isInteger(stage.startMonth) || !Number.isInteger(stage.months) || stage.months < 1 || stage.startMonth < 1 || stage.startMonth + stage.months > 13) throw new Error('Invalid stage period');
    const retention = 1 - churn;
    const growthFactor = churn ? (1 - retention ** stage.months) / churn : stage.months;
    const newPerMonth = (stage.endClients - clients * retention ** stage.months) / growthFactor;
    if (newPerMonth < -1e-8) throw new Error('Target below modeled retention');
    for (let i = 0; i < stage.months; i++, index++) {
      const month = stage.startMonth + i;
      const serial = stage.year * 12 + month;
      if (months.length && serial !== months.at(-1).serial + 1) throw new Error('Non-contiguous months');
      const openingClients = clients;
      const churned = openingClients * churn;
      clients = openingClients - churned + Math.max(0, newPerMonth);
      const averageClients = (openingClients + clients) / 2;
      const recurringRevenue = averageClients * stage.arpu;
      const projectRevenue = stage.projectsPerMonth * stage.projectPrice;
      const contentRevenue = stage.contentPerMonth * stage.contentPrice;
      const appRevenue = stage.paidOrdersPerMonth * p.appPriceExVAT * (1 - p.refundRate);
      const platformFees = appRevenue * p.platformFeeRate;
      const appNet = appRevenue - platformFees;
      const services = projectRevenue + contentRevenue;
      const revenue = recurringRevenue + services + appRevenue;
      const deliveryCosts = recurringRevenue * p.recurringCostRate + projectRevenue * p.projectCostRate + contentRevenue * p.contentCostRate + appRevenue * p.appCostRate;
      const payroll = stage.founderPayMonthly + stage.staffFte * stage.loadedStaffAnnual / 12;
      const overhead = stage.overheadMonthly, marketing = stage.marketingMonthly;
      const operatingExpenses = deliveryCosts + platformFees + payroll + overhead + marketing;
      const ebitda = revenue - operatingExpenses;
      const capex = i === 0 ? stage.capex : 0;
      if (capex) capexLots.push({index, amount:capex});
      const depreciation = capexLots.filter(lot => index - lot.index < p.depreciationMonths).reduce((sum, lot) => sum + lot.amount / p.depreciationMonths, 0);
      const operatingProfit = ebitda - depreciation;
      // Planning reserve, not a tax return; no loss offsets or financing assumed.
      const taxReserve = Math.max(0, operatingProfit) * p.taxReserveRate;
      const netProfit = operatingProfit - taxReserve;
      appNetHistory.push(appNet);
      const appCash = appNetHistory[index - p.appSettlementMonths] || 0;
      const cashReceipts = recurringRevenue + services * p.serviceSameMonthReceipt + previousServices * (1 - p.serviceSameMonthReceipt) + appCash;
      const cashCosts = operatingExpenses - platformFees;
      const operatingCashFlow = cashReceipts - cashCosts - taxReserve;
      const freeCashFlow = operatingCashFlow - capex;
      cumulativeCash += freeCashFlow;
      const receivables = services * (1 - p.serviceSameMonthReceipt) + (p.appSettlementMonths ? appNetHistory.slice(Math.max(0, index - p.appSettlementMonths + 1), index + 1).reduce((a,b) => a+b, 0) : 0);
      const deltaAR = receivables - previousAR;
      const reconciliationError = operatingCashFlow - (netProfit + depreciation - deltaAR);
      const requiredHours = clients * p.recurringHours + stage.projectsPerMonth * p.projectHours + stage.contentPerMonth * p.contentHours;
      const capacityHours = stage.founderDeliveryHours + stage.staffFte * p.staffDeliveryHours;
      const row = {year:stage.year,month,serial,period:`${stage.year}-${String(month).padStart(2,'0')}`,openingClients,clients,averageClients,churned,newClients:Math.max(0,newPerMonth),requiredProspects:Math.max(0,newPerMonth)/closeRate,recurringRevenue,projectRevenue,contentRevenue,appRevenue,revenue,deliveryCosts,platformFees,payroll,overhead,marketing,operatingExpenses,ebitda,depreciation,operatingProfit,taxReserve,netProfit,cashReceipts,cashCosts,operatingCashFlow,capex,freeCashFlow,cumulativeCash,receivables,deltaAR,reconciliationError,requiredHours,capacityHours,capacityGap:Math.max(0,requiredHours-capacityHours),requiredMAU:p.paidConversionRate ? stage.paidOrdersPerMonth/p.paidConversionRate : null,paidOrders:stage.paidOrdersPerMonth};
      months.push(row);
      previousServices = services; previousAR = receivables;
    }
  }
  const sumKeys = ['recurringRevenue','projectRevenue','contentRevenue','appRevenue','revenue','deliveryCosts','platformFees','payroll','overhead','marketing','operatingExpenses','ebitda','depreciation','operatingProfit','taxReserve','netProfit','cashReceipts','cashCosts','operatingCashFlow','capex','freeCashFlow','deltaAR','newClients','churned','requiredProspects','paidOrders'];
  const years = [...new Set(months.map(m=>m.year))].map(year => {
    const rows = months.filter(m=>m.year===year), last=rows.at(-1);
    const result={year,months:rows.length,clients:last.clients,cumulativeCash:last.cumulativeCash,receivables:last.receivables,requiredMAU:last.requiredMAU,capacityGap:Math.max(...rows.map(m=>m.capacityGap))};
    for (const key of sumKeys) result[key]=rows.reduce((sum,row)=>sum+row[key],0);
    result.averageClients=rows.reduce((sum,row)=>sum+row.averageClients,0)/rows.length;
    return result;
  });
  const last=years.at(-1), profit=Math.max(0,last.operatingProfit);
  const minimumCumulativeCash=Math.min(0,...months.map(m=>m.cumulativeCash));
  const totalOpeningLiquidityRequired=Math.max(0,p.cashBuffer-minimumCumulativeCash);
  const openingCash=plan.actuals.openingCashKRW;
  if (openingCash !== null) finite(openingCash,'opening cash');
  const netDebt=plan.actuals.interestBearingDebtKRW;
  if (netDebt !== null) finite(netDebt,'debt');
  return {scenarioKey,months,years,valuationLow:profit*p.valuationMultipleLow,valuationHigh:profit*p.valuationMultipleHigh,minimumCumulativeCash,totalOpeningLiquidityRequired,additionalFundingRequired:openingCash===null?null:Math.max(0,totalOpeningLiquidityRequired-openingCash),endingCash:openingCash===null?null:openingCash+months.at(-1).cumulativeCash,maxReconciliationError:Math.max(...months.map(m=>Math.abs(m.reconciliationError))),firstPositiveOperatingMonth:months.find(m=>m.operatingProfit>0)?.period||null};
}
