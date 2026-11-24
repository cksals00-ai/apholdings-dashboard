-- Only service-role server dispatch receipts. No subscriber data or AI keys.
create table if not exists public.ap_news_startup_receipts (
 issue_date date primary key,
 state text not null default 'requested',
 attempts integer not null default 0 check(attempts between 0 and 3),
 updated_at timestamptz not null default now(),
 last_error text
);
alter table public.ap_news_startup_receipts enable row level security;
revoke all on public.ap_news_startup_receipts from anon,authenticated;
grant all on public.ap_news_startup_receipts to service_role;
create or replace function public.ap_news_startup_claim(p_day date) returns boolean
language plpgsql security definer set search_path=public as $$
begin
 if p_day <> (now() at time zone 'Asia/Seoul')::date then raise exception 'Current Korean date required'; end if;
 insert into ap_news_startup_receipts(issue_date,state,attempts,updated_at) values(p_day,'requesting',1,now())
 on conflict(issue_date) do update set state='requesting',attempts=ap_news_startup_receipts.attempts+1,updated_at=now()
 where ap_news_startup_receipts.attempts<3 and ap_news_startup_receipts.updated_at<now()-interval '15 minutes';
 return found;
end $$;
revoke all on function public.ap_news_startup_claim(date) from public,anon,authenticated;
grant execute on function public.ap_news_startup_claim(date) to service_role;
