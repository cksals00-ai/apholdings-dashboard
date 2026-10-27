begin;
create table b2b_private.login_rate(key text not null,bucket timestamptz not null,total int not null,primary key(key,bucket));
alter table b2b_private.login_rate enable row level security;
revoke all on b2b_private.login_rate from public,anon,authenticated;
grant usage on schema b2b_private to service_role;
grant all on b2b_private.login_rate to service_role;
create function public.b2b_login_limit(p_email_hash text,p_ip_hash text) returns boolean language plpgsql security invoker set search_path='' as $$
declare k text;n int;lim int;begin
 -- Global lock protects rate counters even when concurrent email/IP combinations differ.
 perform pg_advisory_xact_lock(7281027);
 delete from b2b_private.login_rate where bucket<now()-interval '7 days';
 foreach k in array array['global','email:'||p_email_hash,'ip:'||p_ip_hash] loop
  insert into b2b_private.login_rate values(k,date_trunc('hour',now()),1) on conflict(key,bucket) do update set total=b2b_private.login_rate.total+1 returning total into n;
  lim:=case when k='global' then 50 when k like 'email:%' then 3 else 10 end;
  if n>lim then return false;end if;
 end loop;return true;
end $$;
revoke all on function public.b2b_login_limit(text,text) from public,anon,authenticated;
grant execute on function public.b2b_login_limit(text,text) to service_role;
commit;
