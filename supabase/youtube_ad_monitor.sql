-- Private reporting evidence only; no Google credentials, ad mutations or public data.
begin;
create table if not exists public.admin_youtube_ad_observations (
  promotion_id text not null check (promotion_id ~ '^[0-9]+$'),
  observed_at timestamptz not null,
  created_at timestamptz not null default now(),
  source text not null default 'youtube_studio' check (source = 'youtube_studio'),
  video_id text check (video_id ~ '^[A-Za-z0-9_-]{11}$'),
  ad_title text,
  succeeded boolean not null,
  status text,
  cost_krw numeric(16,2) check (cost_krw >= 0),
  impressions bigint check (impressions >= 0),
  views bigint check (views >= 0),
  subscribers bigint check (subscribers >= 0),
  follow_on_views bigint check (follow_on_views >= 0),
  ad_budget_krw numeric(16,2) check (ad_budget_krw >= 0),
  tax_inclusive_cap_krw numeric(16,2) check (tax_inclusive_cap_krw >= 0),
  start_date date,
  end_date date,
  error_code text check (error_code ~ '^[a-z0-9_]{1,120}$'),
  primary key (promotion_id, observed_at),
  check (observed_at <= created_at + interval '5 minutes'),
  check (end_date is null or start_date is null or end_date >= start_date),
  check (succeeded or (status is null and cost_krw is null and impressions is null and views is null and subscribers is null and follow_on_views is null))
);
create index if not exists admin_youtube_ad_observations_time on public.admin_youtube_ad_observations (observed_at desc);
create table if not exists public.admin_youtube_ad_api_checks (
  promotion_id text not null check (promotion_id ~ '^[0-9]+$'),
  observed_at timestamptz not null,
  created_at timestamptz not null default now(),
  source text not null default 'google_ads_api' check (source = 'google_ads_api'),
  customer_id text not null check (customer_id ~ '^[0-9]+$'),
  ok boolean not null,
  report_state text not null check (report_state in ('campaign_unavailable','available','unchecked')),
  campaign_rows integer check (campaign_rows >= 0),
  currency text,
  account_time_zone text,
  api_version text,
  error_code text check (error_code ~ '^[a-z0-9_]{1,120}$'),
  primary key (promotion_id, observed_at),
  check (observed_at <= created_at + interval '5 minutes')
);
create index if not exists admin_youtube_ad_api_checks_time on public.admin_youtube_ad_api_checks (observed_at desc);
alter table public.admin_youtube_ad_observations enable row level security;
alter table public.admin_youtube_ad_api_checks enable row level security;
revoke all on public.admin_youtube_ad_observations, public.admin_youtube_ad_api_checks from anon, authenticated;
grant select on public.admin_youtube_ad_observations, public.admin_youtube_ad_api_checks to authenticated;
grant all on public.admin_youtube_ad_observations, public.admin_youtube_ad_api_checks to service_role;
drop policy if exists youtube_ad_observations_owner_read on public.admin_youtube_ad_observations;
create policy youtube_ad_observations_owner_read on public.admin_youtube_ad_observations for select to authenticated using ((select private.is_admin_portal_owner()));
drop policy if exists youtube_ad_api_checks_owner_read on public.admin_youtube_ad_api_checks;
create policy youtube_ad_api_checks_owner_read on public.admin_youtube_ad_api_checks for select to authenticated using ((select private.is_admin_portal_owner()));
notify pgrst, 'reload schema';
commit;
