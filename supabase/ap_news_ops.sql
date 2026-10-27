-- Private operational alerts, independent of subscriber deliveries.
create table if not exists public.ap_news_ops_events (
 event_key text primary key,event text not null,detail jsonb not null default '{}',
 state text not null default 'pending',attempts int not null default 0,
 provider_id text,last_error text,updated_at timestamptz not null default now(),created_at timestamptz not null default now()
);
alter table public.ap_news_ops_events enable row level security;
revoke all on public.ap_news_ops_events from anon,authenticated;
grant select,insert,update on public.ap_news_ops_events to service_role;
create or replace function public.ap_news_ops_claim(p_key text,p_event text,p_detail jsonb) returns jsonb
language plpgsql security invoker set search_path=public as $$
declare r public.ap_news_ops_events; begin
 if length(p_key)>180 or p_event not in ('test_alert','test_newsletter','test_recovery','ops_alert','ops_recovery') then raise exception 'Invalid operation';end if;
 insert into public.ap_news_ops_events(event_key,event,detail) values(p_key,p_event,p_detail) on conflict do nothing;
 update public.ap_news_ops_events set state='processing',attempts=attempts+1,updated_at=now()
 where event_key=p_key and provider_id is null and attempts<5 and (state in ('pending','retry') or (state='processing' and updated_at<now()-interval '10 minutes')) returning * into r;
 if found then return to_jsonb(r)||'{"claimed":true}'::jsonb;end if;
 select * into r from public.ap_news_ops_events where event_key=p_key;
 return to_jsonb(r)||'{"claimed":false}'::jsonb;
end;$$;
revoke all on function public.ap_news_ops_claim(text,text,jsonb) from public,anon,authenticated;
grant execute on function public.ap_news_ops_claim(text,text,jsonb) to service_role;
notify pgrst,'reload schema';
-- Independent server watchdog, with the existing scheduler secret kept in Vault.
select cron.schedule('ap-news-independent-watch','* * * * *',$job$
 select net.http_post(url:='https://cgijpcimixaregbpvqbf.supabase.co/functions/v1/ap-news-ops',
 headers:=jsonb_build_object('Content-Type','application/json','Authorization','Bearer '||(select decrypted_secret from vault.decrypted_secrets where name='ap_news_scheduler')),
 body:='{"watch":true}'::jsonb,timeout_milliseconds:=30000);
$job$);
