create or replace function public.ap_news_refresh_confirmations() returns integer
language plpgsql security invoker set search_path='' as $$
declare s public.ap_news_subscribers; token text; n integer:=0;
begin
 -- Only requests never attempted during disabled setup are renewed. Sent/failed
 -- confirmations are not automatically resent to an unconfirmed address.
 for s in select a.* from public.ap_news_subscribers a
 where a.status='pending' and a.confirmation_expires<=now()
 and a.consent_at>now()-interval '30 days'
 and exists(select 1 from public.ap_news_deliveries d where d.subscriber_id=a.id and d.kind='confirmation' and d.state='pending' and d.first_attempt_at is null)
 order by a.created_at for update skip locked
 loop
  token:=encode(extensions.gen_random_bytes(32),'hex');
  update public.ap_news_subscribers set confirmation_hash=encode(extensions.digest(token,'sha256'),'hex'),confirmation_expires=now()+interval '48 hours' where id=s.id;
  update public.ap_news_deliveries set state='cancelled',payload='{}' where subscriber_id=s.id and kind='confirmation' and state in ('pending','retry');
  insert into public.ap_news_deliveries(subscriber_id,kind,dedupe_key,payload)
  values(s.id,'confirmation','confirm:'||s.id||':'||encode(extensions.digest(token,'sha256'),'hex'),jsonb_build_object('token',token));
  n:=n+1;
 end loop;
 return n;
end; $$;

create or replace function public.ap_news_unsubscribe(p_id uuid) returns boolean
language plpgsql security invoker set search_path='' as $$
begin
 perform 1 from public.ap_news_subscribers where id=p_id for update;
 if not found then return false; end if;
 update public.ap_news_subscribers set status='unsubscribed',unsubscribed_at=now(),confirmation_hash=null,confirmation_expires=null where id=p_id;
 update public.ap_news_deliveries set state='cancelled',payload='{}' where subscriber_id=p_id and state in ('pending','retry','processing');
 return true;
end; $$;
revoke all on function public.ap_news_refresh_confirmations(),public.ap_news_unsubscribe(uuid) from public,anon,authenticated;
grant execute on function public.ap_news_refresh_confirmations(),public.ap_news_unsubscribe(uuid) to service_role;

create or replace function public.ap_news_authorize_delivery(p_id uuid) returns boolean
language plpgsql security invoker set search_path='' as $$
declare s public.ap_news_subscribers; d public.ap_news_deliveries;
begin
 -- Consistent subscriber -> delivery lock order with unsubscribe/resubscribe.
 select a.* into s from public.ap_news_subscribers a where a.id=(select subscriber_id from public.ap_news_deliveries where id=p_id) for update;
 if not found then return false; end if;
 select * into d from public.ap_news_deliveries where id=p_id for update;
 if not found or d.state<>'processing' then return false; end if;
 if d.kind='confirmation' then
  return s.status='pending' and s.confirmation_expires>now()
   and s.confirmation_hash=encode(extensions.digest(d.payload->>'token','sha256'),'hex');
 end if;
 return s.status='active' and exists(select 1 from public.ap_news_issues i where i.issue_date=d.issue_date and i.status='published' and i.verified);
end; $$;
revoke all on function public.ap_news_authorize_delivery(uuid) from public,anon,authenticated;
grant execute on function public.ap_news_authorize_delivery(uuid) to service_role;
