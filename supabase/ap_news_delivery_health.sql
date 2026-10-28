-- Read-only whole-issue completion signal. Never exposes recipients or sends mail.
create or replace function public.ap_news_delivery_health(p_day date)
returns jsonb language sql stable security invoker set search_path=public,pg_temp as $$
 select jsonb_build_object('active',(select count(*) from public.ap_news_subscribers where status='active' and confirmed_at is not null))
 || coalesce((select to_jsonb(s)-'issue_date'-'last_attempted_at' from public.ap_news_delivery_summary s where issue_date=p_day),'{"accepted":0}'::jsonb);
$$;
revoke all on function public.ap_news_delivery_health(date) from public,anon,authenticated;
grant execute on function public.ap_news_delivery_health(date) to service_role;
notify pgrst,'reload schema';
