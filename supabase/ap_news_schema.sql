-- AP News data is service-only. The existing owner accesses counts through the Edge Function.
create table public.ap_news_subscribers (
 id uuid primary key default gen_random_uuid(),
 email text not null unique check(length(email)<=254),
 name text not null default '', locale text not null default 'ko' check(locale='ko'),
 status text not null default 'pending' check(status in ('pending','active','unsubscribed')),
 consent_at timestamptz not null default now(), consent_version text not null default '2026-10-09',
 confirmation_hash text, confirmation_expires timestamptz,
 confirmed_at timestamptz, unsubscribed_at timestamptz, created_at timestamptz not null default now()
);
create table public.ap_news_issues (
 issue_date date primary key, number integer not null unique check(number>0), title text not null,
 status text not null default 'draft' check(status in ('draft','published')),
 verified boolean not null default false, web_url text not null, pdf_url text not null,
 email_html text not null, source_data jsonb not null,
 publish_at timestamptz not null, created_at timestamptz not null default now(),
 check(status<>'published' or verified)
);
create table public.ap_news_deliveries (
 id uuid primary key default gen_random_uuid(), subscriber_id uuid not null references public.ap_news_subscribers(id) on delete cascade,
 issue_date date references public.ap_news_issues(issue_date), kind text not null check(kind in ('confirmation','newsletter')),
 dedupe_key text not null unique, payload jsonb not null default '{}',
 state text not null default 'pending' check(state in ('pending','processing','retry','sent','cancelled','failed','uncertain')),
 attempts integer not null default 0, first_attempt_at timestamptz, attempted_at timestamptz, next_attempt_at timestamptz not null default now(),
 provider_id text, last_error text, created_at timestamptz not null default now(),
 check((kind='confirmation' and issue_date is null) or (kind='newsletter' and issue_date is not null))
);
create index ap_news_delivery_queue on public.ap_news_deliveries(state,next_attempt_at);
create index ap_news_delivery_subscriber on public.ap_news_deliveries(subscriber_id);
create index ap_news_delivery_issue on public.ap_news_deliveries(issue_date);
create table public.ap_news_requests (key_hash text not null,bucket timestamptz not null,total integer not null default 1,primary key(key_hash,bucket));
create table public.ap_news_runtime (id text primary key default 'mail' check(id='mail'),mail_ready boolean not null default false,status text not null default 'setup_required',last_run timestamptz,last_error text);
insert into public.ap_news_runtime(id) values('mail');
create table public.ap_news_scheduler_auth(id text primary key check(id='scheduler'),token_hash text not null);

alter table public.ap_news_subscribers enable row level security;
alter table public.ap_news_issues enable row level security;
alter table public.ap_news_deliveries enable row level security;
alter table public.ap_news_requests enable row level security;
alter table public.ap_news_runtime enable row level security;
alter table public.ap_news_scheduler_auth enable row level security;
revoke all on public.ap_news_subscribers,public.ap_news_issues,public.ap_news_deliveries,public.ap_news_requests,public.ap_news_runtime,public.ap_news_scheduler_auth from anon,authenticated;
grant all on public.ap_news_subscribers,public.ap_news_issues,public.ap_news_deliveries,public.ap_news_requests,public.ap_news_runtime,public.ap_news_scheduler_auth to service_role;

create function public.ap_news_rate_limit(p_key text,p_limit integer) returns boolean
language plpgsql security invoker set search_path='' as $$
declare n integer;
begin
 insert into public.ap_news_requests(key_hash,bucket) values(p_key,date_trunc('hour',now()))
 on conflict(key_hash,bucket) do update set total=public.ap_news_requests.total+1 returning total into n;
 return n<=p_limit;
end; $$;

create function public.ap_news_request_subscription(p_email text,p_name text) returns void
language plpgsql security invoker set search_path='' as $$
declare s public.ap_news_subscribers; token text;
begin
 insert into public.ap_news_subscribers(email,name) values(p_email,p_name) on conflict(email) do nothing;
 select * into s from public.ap_news_subscribers where email=p_email for update;
 if s.status='active' then return; end if;
 if s.status='pending' and s.confirmation_expires>now() then return; end if;
 token:=encode(extensions.gen_random_bytes(32),'hex');
 update public.ap_news_subscribers set name=p_name,status='pending',consent_at=now(),unsubscribed_at=null,
 confirmation_hash=encode(extensions.digest(token,'sha256'),'hex'),confirmation_expires=now()+interval '48 hours'
 where id=s.id;
 update public.ap_news_deliveries set state='cancelled',payload='{}' where subscriber_id=s.id and kind='confirmation' and state in ('pending','retry');
 insert into public.ap_news_deliveries(subscriber_id,kind,dedupe_key,payload)
 values(s.id,'confirmation','confirm:'||s.id||':'||token,jsonb_build_object('token',token));
end; $$;

create function public.ap_news_confirm(p_hash text) returns boolean
language plpgsql security invoker set search_path='' as $$
declare n integer;
begin
 update public.ap_news_subscribers set status='active',confirmed_at=now(),confirmation_hash=null,confirmation_expires=null
 where status='pending' and confirmation_hash=p_hash and confirmation_expires>now();
 get diagnostics n=row_count;return n=1;
end; $$;

create function public.ap_news_enqueue() returns integer
language plpgsql security invoker set search_path='' as $$
declare n integer;
begin
 insert into public.ap_news_deliveries(subscriber_id,issue_date,kind,dedupe_key)
 select s.id,i.issue_date,'newsletter','issue:'||i.issue_date||':'||s.id
 from public.ap_news_subscribers s cross join public.ap_news_issues i
 where s.status='active' and i.status='published' and i.verified and i.publish_at<=now()
 and i.issue_date=(now() at time zone 'Asia/Seoul')::date
 on conflict(dedupe_key) do nothing;
 get diagnostics n=row_count;return n;
end; $$;

create function public.ap_news_claim(p_limit integer default 10) returns setof public.ap_news_deliveries
language plpgsql security invoker set search_path='' as $$
begin
 -- Resend idempotency expires after 24h. Never retry an ambiguous submission beyond its window.
 update public.ap_news_deliveries set state='uncertain',last_error='provider_result_requires_review'
 where state in ('processing','retry') and first_attempt_at<now()-interval '23 hours';
 update public.ap_news_deliveries d set state='cancelled',payload='{}'
 from public.ap_news_subscribers s where s.id=d.subscriber_id and d.state in ('pending','retry','processing')
 and ((d.kind='newsletter' and s.status<>'active') or (d.kind='confirmation' and (s.status<>'pending' or s.confirmation_expires<=now())));
 return query
 update public.ap_news_deliveries d set state='processing',attempts=d.attempts+1,
 first_attempt_at=coalesce(d.first_attempt_at,now()),attempted_at=now()
 where d.id in (
  select q.id from public.ap_news_deliveries q
  where ((q.state in ('pending','retry') and q.next_attempt_at<=now()) or (q.state='processing' and q.attempted_at<now()-interval '10 minutes'))
  and q.attempts<5 order by q.created_at for update skip locked limit least(greatest(p_limit,1),10)
 ) returning d.*;
end; $$;

revoke all on function public.ap_news_rate_limit(text,integer),public.ap_news_request_subscription(text,text),public.ap_news_confirm(text),public.ap_news_enqueue(),public.ap_news_claim(integer) from public,anon,authenticated;
grant execute on function public.ap_news_rate_limit(text,integer),public.ap_news_request_subscription(text,text),public.ap_news_confirm(text),public.ap_news_enqueue(),public.ap_news_claim(integer) to service_role;

-- Secret is generated and kept in Vault; no client sees its value.
do $$
declare token text;
begin
 token:=encode(extensions.gen_random_bytes(32),'hex');
 perform vault.create_secret(token,'ap_news_scheduler','AP News internal queue authentication');
 insert into public.ap_news_scheduler_auth(id,token_hash) values('scheduler',encode(extensions.digest(token,'sha256'),'hex'));
end; $$;

select cron.schedule('ap-news-mail-queue','*/5 * * * *',$job$
 select net.http_post(
 url:='https://cgijpcimixaregbpvqbf.supabase.co/functions/v1/ap-news/dispatch',
 headers:=jsonb_build_object('Content-Type','application/json','Authorization','Bearer '||(select decrypted_secret from vault.decrypted_secrets where name='ap_news_scheduler')),
 body:='{}'::jsonb,timeout_milliseconds:=20000
 );
$job$);
select cron.schedule('ap-news-retention','15 18 * * *',$job$
 delete from public.ap_news_subscribers where (status='unsubscribed' and unsubscribed_at<now()-interval '30 days') or (status='pending' and consent_at<now()-interval '30 days');
 delete from public.ap_news_requests where bucket<now()-interval '7 days';
$job$);
