-- Apply only after deployment approval. No operating data is copied.
begin;
create schema if not exists b2b_private;
revoke all on schema b2b_private from public,anon;
grant usage on schema b2b_private to authenticated;
create function b2b_private.is_owner() returns boolean language sql stable security invoker set search_path='' as $$
 select auth.uid()='94f18e51-cc1e-46c5-b2e0-235bf9221761'::uuid
$$;
create function b2b_private.verified_email() returns text language plpgsql stable security definer set search_path='' as $$
declare e text;begin
 select lower(email) into e from auth.users where id=auth.uid() and email_confirmed_at is not null;
 if e is null then raise exception '회사 이메일을 먼저 확인해 주세요.'; end if;return e;
end $$;
revoke all on all functions in schema b2b_private from public,anon;
grant execute on all functions in schema b2b_private to authenticated;
create table public.b2b_applications(
 id uuid primary key default gen_random_uuid(), user_id uuid not null unique references auth.users(id),
 product text not null default 'hajeung' check(product='hajeung'),email text not null,
 name text not null check(length(name) between 1 and 60),company text not null check(length(company) between 1 and 100),device text not null check(device in ('ios','android','both')),
 status text not null default 'pending' check(status in ('pending','approved','held','rejected','issued')),
 member_id uuid,created_at timestamptz not null default now(),updated_at timestamptz not null default now()
);
create table public.b2b_requests(
 id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id),application_id uuid not null references public.b2b_applications(id),
 kind text not null check(kind in ('bug','improvement','question')),title text not null check(length(title) between 2 and 120),body text not null check(length(body) between 5 and 4000),
 screen text not null default '' check(length(screen)<=100),version text not null default '' check(length(version)<=80),device text not null default '' check(length(device)<=120),
 status text not null default 'received' check(status in ('received','reviewing','working','needs_info','done')),created_at timestamptz not null default now(),updated_at timestamptz not null default now()
);
create index b2b_requests_user_created on public.b2b_requests(user_id,created_at desc);
create table public.b2b_replies(id uuid primary key default gen_random_uuid(),request_id uuid not null references public.b2b_requests(id),author_id uuid not null references auth.users(id),is_staff boolean not null,body text not null check(length(body) between 1 and 4000),created_at timestamptz not null default now());
create index b2b_replies_request on public.b2b_replies(request_id,created_at);
create table b2b_private.audit(id bigint generated always as identity primary key,actor_id uuid not null,entity_id uuid not null,event text not null,at timestamptz not null default now());
alter table b2b_private.audit enable row level security;
revoke all on b2b_private.audit from public,anon,authenticated;
alter table public.b2b_applications enable row level security;alter table public.b2b_requests enable row level security;alter table public.b2b_replies enable row level security;
revoke all on public.b2b_applications,public.b2b_requests,public.b2b_replies from public,anon,authenticated;
grant select on public.b2b_applications,public.b2b_requests,public.b2b_replies to authenticated;
create policy b2b_app_read on public.b2b_applications for select to authenticated using(user_id=(select auth.uid()) or (select b2b_private.is_owner()));
create policy b2b_request_read on public.b2b_requests for select to authenticated using(user_id=(select auth.uid()) or (select b2b_private.is_owner()));
create policy b2b_reply_read on public.b2b_replies for select to authenticated using(exists(select 1 from public.b2b_requests r where r.id=request_id and (r.user_id=(select auth.uid()) or (select b2b_private.is_owner()))));

create function public.b2b_apply(p_name text,p_company text,p_device text) returns uuid language plpgsql security definer set search_path='' as $$
declare e text;out_id uuid;begin
 e:=b2b_private.verified_email();
 insert into public.b2b_applications(user_id,email,name,company,device) values(auth.uid(),e,trim(p_name),trim(p_company),p_device) returning id into out_id;
 insert into b2b_private.audit(actor_id,entity_id,event) values(auth.uid(),out_id,'application.created');return out_id;
end $$;
create function public.b2b_request(p_kind text,p_title text,p_body text,p_screen text,p_version text,p_device text) returns uuid language plpgsql security definer set search_path='' as $$
declare a uuid;out_id uuid;begin
 perform b2b_private.verified_email();perform pg_advisory_xact_lock(hashtext(auth.uid()::text));
 select id into a from public.b2b_applications where user_id=auth.uid();if a is null then raise exception '먼저 테스트 계정을 신청해 주세요.';end if;
 if (select count(*) from public.b2b_requests where user_id=auth.uid() and created_at>now()-interval '1 hour')>=10 then raise exception '잠시 후 다시 요청해 주세요.';end if;
 insert into public.b2b_requests(user_id,application_id,kind,title,body,screen,version,device) values(auth.uid(),a,p_kind,trim(p_title),trim(p_body),p_screen,p_version,p_device) returning id into out_id;
 return out_id;
end $$;
create function public.b2b_reply(p_request uuid,p_body text) returns void language plpgsql security definer set search_path='' as $$
begin
 perform b2b_private.verified_email();perform pg_advisory_xact_lock(hashtext(auth.uid()::text));
 if not exists(select 1 from public.b2b_requests where id=p_request and (user_id=auth.uid() or b2b_private.is_owner())) then raise exception '요청을 찾을 수 없습니다.';end if;
 if (select count(*) from public.b2b_replies where author_id=auth.uid() and created_at>now()-interval '1 hour')>=30 then raise exception '잠시 후 다시 답변해 주세요.';end if;
 insert into public.b2b_replies(request_id,author_id,is_staff,body) values(p_request,auth.uid(),b2b_private.is_owner(),trim(p_body));
end $$;
create function public.b2b_application_status(p_id uuid,p_status text) returns void language plpgsql security definer set search_path='' as $$
begin
 if not coalesce(b2b_private.is_owner(),false) then raise exception '관리자만 처리할 수 있습니다.';end if;
 if p_status not in ('approved','held','rejected') then raise exception '상태를 확인해 주세요.';end if;
 update public.b2b_applications set status=p_status,updated_at=now() where id=p_id and status<>'issued';if not found then raise exception '처리 가능한 신청이 없습니다.';end if;
 insert into b2b_private.audit(actor_id,entity_id,event) values(auth.uid(),p_id,'application.'||p_status);
end $$;
create function public.b2b_request_status(p_id uuid,p_status text) returns void language plpgsql security definer set search_path='' as $$
begin
 if not coalesce(b2b_private.is_owner(),false) then raise exception '관리자만 처리할 수 있습니다.';end if;
 update public.b2b_requests set status=p_status,updated_at=now() where id=p_id;if not found then raise exception '요청을 찾을 수 없습니다.';end if;
 insert into b2b_private.audit(actor_id,entity_id,event) values(auth.uid(),p_id,'request.'||p_status);
end $$;
-- Invoked only by a human administrator. Returns the code once; never stores it in the support tables.
create function public.b2b_issue_code(p_id uuid) returns jsonb language plpgsql security definer set search_path='' as $$
declare a public.b2b_applications;code text;member uuid;begin
 if not coalesce(b2b_private.is_owner(),false) then raise exception '관리자만 발급할 수 있습니다.';end if;
 select * into a from public.b2b_applications where id=p_id for update;
 if a.id is null or a.status<>'approved' then raise exception '승인된 미발급 신청만 발급할 수 있습니다.';end if;
 -- Do not overwrite any existing app identity, demo or operating.
 if exists(select 1 from hajeung.members where email=a.email) then raise exception '기존 앱 계정이 있습니다. 별도 확인이 필요합니다.';end if;
 code:=upper(substr(replace(gen_random_uuid()::text,'-',''),1,12));
 insert into hajeung.members(email,name,role,active,demo,code_hash,code_issued_at) values(a.email,a.name,'담당자',true,true,encode(sha256(convert_to(code,'UTF8')),'hex'),now()) returning id into member;
 update public.b2b_applications set status='issued',member_id=member,updated_at=now() where id=p_id;
 insert into b2b_private.audit(actor_id,entity_id,event) values(auth.uid(),p_id,'application.code_issued');
 return jsonb_build_object('email',a.email,'code',code);
end $$;
revoke all on function public.b2b_apply(text,text,text),public.b2b_request(text,text,text,text,text,text),public.b2b_reply(uuid,text),public.b2b_application_status(uuid,text),public.b2b_request_status(uuid,text),public.b2b_issue_code(uuid) from public,anon;
grant execute on function public.b2b_apply(text,text,text),public.b2b_request(text,text,text,text,text,text),public.b2b_reply(uuid,text),public.b2b_application_status(uuid,text),public.b2b_request_status(uuid,text),public.b2b_issue_code(uuid) to authenticated;

insert into storage.buckets(id,name,public,file_size_limit,allowed_mime_types) values('hajeung-support','hajeung-support',false,5242880,array['image/jpeg']);
create policy b2b_photo_insert on storage.objects for insert to authenticated with check(bucket_id='hajeung-support' and exists(select 1 from public.b2b_requests r where r.user_id=auth.uid() and name=auth.uid()::text||'/'||r.id::text||'/photo.jpg'));
create policy b2b_photo_read on storage.objects for select to authenticated using(bucket_id='hajeung-support' and exists(select 1 from public.b2b_requests r where name=r.user_id::text||'/'||r.id::text||'/photo.jpg' and (r.user_id=auth.uid() or b2b_private.is_owner())));
commit;
