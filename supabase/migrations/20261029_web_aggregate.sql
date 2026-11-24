create table public.web_analytics_daily (
 day date not null,
 host text not null check(host in ('www.apholdings.kr','apholdings.kr','edu.apholdings.kr','games.apholdings.kr','ent.apholdings.kr','shop.apholdings.kr','sports.apholdings.kr')),
 event text not null check(event in ('page_view','courtmate_blog_arrival','ap_install_test')),
 count bigint not null default 0 check(count >= 0),
 primary key(day,host,event)
);
alter table public.web_analytics_daily enable row level security;
revoke all on public.web_analytics_daily from anon,authenticated;
grant select,insert,update on public.web_analytics_daily to service_role;
create function public.record_web_aggregate(p_host text,p_event text) returns void
language sql security definer set search_path='' as $$
 insert into public.web_analytics_daily(day,host,event,count)
 values ((now() at time zone 'Asia/Seoul')::date,p_host,p_event,1)
 on conflict(day,host,event) do update set count=public.web_analytics_daily.count+1;
$$;
revoke all on function public.record_web_aggregate(text,text) from public,anon,authenticated;
grant execute on function public.record_web_aggregate(text,text) to service_role;
comment on table public.web_analytics_daily is 'Daily aggregate counts only. No IP, user agent, cookies, user IDs, referrers, paths or individual event records. Install-test events excluded from reports.';
