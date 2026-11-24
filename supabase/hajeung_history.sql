begin;
create table public.b2b_change_history(
 id uuid primary key default gen_random_uuid(),record_key text not null unique check(length(record_key) between 1 and 100),request_id uuid references public.b2b_requests(id),
 title text not null check(length(title) between 2 and 120),detail text not null check(length(detail) between 5 and 4000),
 apple_version text not null default '' check(length(apple_version)<=80),android_version text not null default '' check(length(android_version)<=80),
 platform text not null check(platform in ('both','ios','android','server','web')),kind text not null check(kind in ('request','fix','release','customer_check')),
 status text not null check(status in ('received','working','released','customer_check','done')),occurred_on date not null,completed_on date,
 actor text not null,created_at timestamptz not null default now(),check(status<>'done' or completed_on is not null)
);
alter table public.b2b_change_history enable row level security;
revoke all on public.b2b_change_history from public,anon,authenticated;
grant select on public.b2b_change_history to authenticated;
create policy b2b_history_owner_read on public.b2b_change_history for select to authenticated using((select b2b_private.is_owner()));
create or replace function public.b2b_history_add(p jsonb)returns uuid language plpgsql security definer set search_path='' as $$
declare e text;out_id uuid;existing public.b2b_change_history;begin
 if not coalesce(b2b_private.is_owner(),false) then raise exception '관리자만 기록할 수 있습니다.';end if;
 e:=b2b_private.verified_email();
 insert into public.b2b_change_history(record_key,request_id,title,detail,apple_version,android_version,platform,kind,status,occurred_on,completed_on,actor)
 values(p->>'record_key',nullif(p->>'request_id','')::uuid,trim(p->>'title'),trim(p->>'detail'),coalesce(p->>'apple_version',''),coalesce(p->>'android_version',''),p->>'platform',p->>'kind',p->>'status',(p->>'occurred_on')::date,nullif(p->>'completed_on','')::date,e)
 on conflict(record_key)do nothing returning id into out_id;
 if out_id is null then
 select * into existing from public.b2b_change_history where record_key=p->>'record_key';
 if (existing.request_id,existing.title,existing.detail,existing.apple_version,existing.android_version,existing.platform,existing.kind,existing.status,existing.occurred_on,existing.completed_on)
 is distinct from (nullif(p->>'request_id','')::uuid,trim(p->>'title'),trim(p->>'detail'),coalesce(p->>'apple_version',''),coalesce(p->>'android_version',''),p->>'platform',p->>'kind',p->>'status',(p->>'occurred_on')::date,nullif(p->>'completed_on','')::date)
 then raise exception '이전 저장 요청과 내용이 다릅니다. 새로고침으로 저장 여부를 확인한 뒤 새 기록을 추가해 주세요.' ;end if;
 out_id:=existing.id;
 end if;
 return out_id;
end $$;
create function public.b2b_request_timeline(p_id uuid)returns jsonb language plpgsql stable security definer set search_path='' as $$
declare result jsonb;begin
 if not coalesce(b2b_private.is_owner(),false)then raise exception '관리자만 이력을 볼 수 있습니다.';end if;
 perform b2b_private.verified_email();
 select coalesce(jsonb_agg(x order by x.at),'[]'::jsonb) into result from (
 select a.at,a.event as title,a.actor_id::text as actor,''::text as detail from b2b_private.audit a where a.entity_id=p_id
 union all select h.created_at,h.title,h.actor,h.detail from public.b2b_change_history h where h.request_id=p_id) x;
 return result;
end $$;
revoke all on function public.b2b_history_add(jsonb),public.b2b_request_timeline(uuid) from public,anon;
grant execute on function public.b2b_history_add(jsonb),public.b2b_request_timeline(uuid) to authenticated;
commit;
