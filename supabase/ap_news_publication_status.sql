-- API-free newsletter publication evidence. Service-only writes/reads;
-- the existing owner-authenticated Edge endpoint is the sole browser gateway.
begin;
create table if not exists public.ap_news_publication_runs (
 issue_date date primary key,
 title text, number integer,
 ready_at timestamptz, ready_verified_at timestamptz,
 bundle_filename text, bundle_sha256 text,
 publication_started_at timestamptz, deployed_at timestamptz,
 public_verified_at timestamptz, registered_at timestamptz,
 last_state text not null default 'waiting' check(last_state in ('waiting','ready','publishing','published','error')),
 last_error text, workflow_url text,
 last_checked_at timestamptz not null default now()
);
alter table public.ap_news_publication_runs enable row level security;
revoke all on public.ap_news_publication_runs from public, anon, authenticated;
grant select,insert,update on public.ap_news_publication_runs to service_role;

create or replace function public.ap_news_record_publication(p_day date,p_event text,p_metadata jsonb default '{}'::jsonb)
returns jsonb language plpgsql security invoker set search_path=public,pg_temp as $$
declare result public.ap_news_publication_runs; desired text;
begin
 if p_event not in ('handoff','waiting','started','deployed','published','error') then
  raise exception 'Invalid publication event';
 end if;
 if p_event='handoff' and (
  coalesce(p_metadata->>'bundle_sha256','') !~ '^[a-f0-9]{64}$' or
  coalesce(p_metadata->>'bundle_filename','') <> 'AP-News-'||p_day::text||'-ready.zip'
 ) then raise exception 'Verified bundle evidence required'; end if;
 desired:=case p_event when 'handoff' then 'ready' when 'waiting' then 'waiting'
  when 'published' then 'published' when 'error' then 'error' else 'publishing' end;
 insert into public.ap_news_publication_runs as old(
  issue_date,title,number,ready_at,ready_verified_at,bundle_filename,bundle_sha256,
  publication_started_at,deployed_at,public_verified_at,registered_at,last_state,last_error,workflow_url,last_checked_at
 ) values (
  p_day,nullif(left(p_metadata->>'title',200),''),nullif(p_metadata->>'number','')::integer,
  case when p_event='handoff' then now() end,case when p_event='handoff' then now() end,
  case when p_event='handoff' then p_metadata->>'bundle_filename' end,
  case when p_event='handoff' then p_metadata->>'bundle_sha256' end,
  case when p_event='started' then now() end,case when p_event='deployed' then now() end,
  case when p_event='published' then now() end,case when p_event='published' then now() end,
  desired,case when p_event='error' then left(coalesce(p_metadata->>'last_error','서버 처리 오류'),500) end,
  case when p_metadata->>'workflow_url' ~ '^https://github.com/cksals00-ai/apholdings-dashboard/actions/runs/[0-9]+$' then p_metadata->>'workflow_url' end,now()
 ) on conflict(issue_date) do update set
  title=coalesce(excluded.title,old.title),number=coalesce(excluded.number,old.number),
  ready_at=coalesce(old.ready_at,excluded.ready_at),ready_verified_at=coalesce(excluded.ready_verified_at,old.ready_verified_at),
  bundle_filename=coalesce(excluded.bundle_filename,old.bundle_filename),bundle_sha256=coalesce(excluded.bundle_sha256,old.bundle_sha256),
  publication_started_at=coalesce(old.publication_started_at,excluded.publication_started_at),
  deployed_at=coalesce(excluded.deployed_at,old.deployed_at),
  public_verified_at=coalesce(excluded.public_verified_at,old.public_verified_at),
  registered_at=coalesce(old.registered_at,excluded.registered_at),
  last_state=case when old.registered_at is not null then 'published' else excluded.last_state end,
  last_error=excluded.last_error,workflow_url=coalesce(excluded.workflow_url,old.workflow_url),last_checked_at=now()
 returning * into result;
 return to_jsonb(result);
end $$;
revoke all on function public.ap_news_record_publication(date,text,jsonb) from public,anon,authenticated;
grant execute on function public.ap_news_record_publication(date,text,jsonb) to service_role;

create or replace view public.ap_news_delivery_summary with (security_invoker=true) as
 select issue_date,count(*)::int total,
  count(*) filter(where provider_id is not null)::int accepted,
  count(*) filter(where state='pending')::int pending,
  count(*) filter(where state='processing')::int processing,
  count(*) filter(where state='retry')::int retry,
  count(*) filter(where state='failed')::int failed,
  count(*) filter(where state='uncertain')::int uncertain,
  count(*) filter(where state='sent' and provider_id is null)::int unconfirmed,
  count(*) filter(where state='cancelled' and provider_id is null)::int cancelled,
  max(attempted_at) last_attempted_at
 from public.ap_news_deliveries where kind='newsletter' group by issue_date;
revoke all on public.ap_news_delivery_summary from public,anon,authenticated;
grant select on public.ap_news_delivery_summary to service_role;

create or replace function public.ap_news_admin_pipeline()
returns jsonb language sql stable security invoker set search_path=public,pg_temp as $$
 select jsonb_build_object(
  'today',(now() at time zone 'Asia/Seoul')::date,
  'checked_at',now(),
  'runs',coalesce((select jsonb_agg(to_jsonb(t)) from (
   select * from public.ap_news_publication_runs order by issue_date desc limit 30
  ) t),'[]'::jsonb),
  'delivery_summary',coalesce((select jsonb_agg(to_jsonb(t)) from (
   select * from public.ap_news_delivery_summary order by issue_date desc limit 40
  ) t),'[]'::jsonb)
 );
$$;
revoke all on function public.ap_news_admin_pipeline() from public,anon,authenticated;
grant execute on function public.ap_news_admin_pipeline() to service_role;
notify pgrst,'reload schema';
commit;
