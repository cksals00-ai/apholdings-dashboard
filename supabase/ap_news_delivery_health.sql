-- Read-only whole-issue completion signal. Never exposes recipients or sends mail.
create or replace function public.ap_news_delivery_health(p_day date)
returns jsonb language sql stable security invoker set search_path=public,pg_temp as $$
 select jsonb_build_object('active',(select count(*) from public.ap_news_subscribers where status='active' and confirmed_at is not null),
 'eligible_missing',(select count(*) from public.ap_news_subscribers a where a.status='active' and a.confirmed_at is not null and not exists(select 1 from public.ap_news_deliveries d where d.subscriber_id=a.id and d.issue_date=p_day and d.kind='newsletter' and d.provider_id is not null)))
 || coalesce((select to_jsonb(s)-'issue_date'-'last_attempted_at' from public.ap_news_delivery_summary s where issue_date=p_day),'{"accepted":0}'::jsonb);
$$;
revoke all on function public.ap_news_delivery_health(date) from public,anon,authenticated;
grant execute on function public.ap_news_delivery_health(date) to service_role;
notify pgrst,'reload schema';
