create table public.admin_business_plans (
  id text primary key,
  payload jsonb not null check (jsonb_typeof(payload) = 'object'),
  updated_at timestamptz not null default now()
);
alter table public.admin_business_plans enable row level security;
alter table public.admin_business_plans force row level security;
revoke all on table public.admin_business_plans from public, anon, authenticated;
grant select on table public.admin_business_plans to authenticated;
grant all on table public.admin_business_plans to service_role;
create policy admin_business_plans_owner_read on public.admin_business_plans
  for select to authenticated
  using ((select private.is_admin_portal_owner()));
comment on table public.admin_business_plans is 'Owner-only planning snapshots. Never include payloads in public site source or static exports.';
