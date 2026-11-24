# Owner-only business planning module

Entry point: `/admin/#plan`. Reuses the existing owner login and navigation.
This is a management planning snapshot, not a ledger, a market valuation,
an automated trading system, or an automatically refreshed operating forecast.

## Source and privacy

- The static site repository is public. Never commit business payloads,
  forecast outputs, screenshots containing private data, or credentials here.
- The client reads `admin_business_plans` by snapshot ID only after login.
- The migration grants authenticated SELECT, with the existing
  `private.is_admin_portal_owner()` allowlist policy. Anonymous access and
  client-side writes are not granted. No new owner identities are created.
- Update reviewed snapshots through an authorized administrative database
  workflow. Keep `schemaVersion`, `version`, `asOf`, and source references.
- Logout clears the snapshot and invalidates pending requests. CSV/JSON
  downloads are explicit owner actions; no private browser storage is used
  by this module. The existing authentication client keeps its normal session.

## Model

`admin/business-plan-model.mjs` is a pure, dependency-free calculation engine.
All money is KRW. Stages are contiguous calendar periods. Monthly acquisition
is solved from beginning clients, churn, and the target ending client count.
Mid-month average clients earn recurring revenue. Fractional clients and FTEs
are planning equivalents, not recorded customers or employees.

Revenue excludes VAT and app refunds. Platform fees are P&L expenses; app
cash receipts are net of fees and delayed by the configured settlement lag.
Services use current/next month collection weights. All remaining costs are
paid in the same month. Capex is incurred at the start of a stage and uses
straight-line monthly depreciation. Tax is a reserve on positive monthly
operating income, not jurisdiction-specific tax advice or a tax return.

Reconciliation: operating cash flow = net income + depreciation − change in
receivables; free cash flow = operating cash flow − capital expenditures.
Unknown opening cash remains null. The liquidity requirement is the minimum
opening cash required to avoid falling below the buffer over the plan, not a
claim that financing has been secured. EV uses positive operating profit and
explicit internal multipliers; current asset assumptions are not added to it.

## Visual contract

This module uses the existing admin's DOM/CSS dashboard bar primitives, not a
separate hosted dashboard. Comparisons use five annual categories, grouped
revenue/profit bars and a separate cumulative cash series. Signed bars share a
zero axis. Blue/teal plus neutral text, direct values and separate series labels
provide non-color encoding. Tables carry exact rounded totals and source notes.
The three scenarios use the same model; a scenario selection updates every tab.
Responsive rules stack cards/charts; wide numeric tables remain horizontally
scrollable. Do not publish a private local QA harness to GitHub Pages.

## Validation and release

```sh
node --check admin/admin.js
node --check admin/business-plan.js
node scripts/test_business_plan.mjs
# Optional: supply an authorized private snapshot path OUTSIDE this repository.
node scripts/test_business_plan.mjs /absolute/private/plan-snapshot.json
node scripts/test_business_plan_ui.mjs /absolute/private/plan-snapshot.json
python3 scripts/check_site.py
bash -n deploy_dashboard.sh
```

Verify RLS and grants, anonymous denial, authenticated non-owner empty result,
and owner rendering through a legitimate session. Component tests cover
all scenario/tab states, error recovery, escaping and the logout response race.
They do not substitute for a logged-in desktop/mobile visual check.

Before releasing, fetch the remote branch and preserve concurrent changes.
The owner's separate Mac sync source must include these admin files and changes
before the next source sync, or an older `admin/index.html` / `admin.js` could
remove the navigation entry. The website content-version guard alone does not
detect admin-only changes. Do not change the Mac source or its automation as
part of this module without access to that source and an explicit scope.
