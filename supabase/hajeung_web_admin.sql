begin;
create or replace function b2b_private.mail_state() returns jsonb language sql stable security definer set search_path='' as $$
 select jsonb_build_object('days',r.days,'active',r.active,'subject',r.subject,'body',r.body,
 'recipient',coalesce((select value from hajeung.settings where key='default_mail_to'),''),
 'name',coalesce((select value from hajeung.settings where key='default_mail_name'),''),
 'mode',coalesce((select value from hajeung.settings where key='send_mode'),'승인'))
 from hajeung.mail_rules r where r.key='D60'
$$;
revoke all on function b2b_private.mail_state() from public,anon,authenticated;
create or replace function public.hajeung_web_context() returns jsonb language plpgsql stable security definer set search_path='' as $$
begin
 perform b2b_private.verified_email();
 return jsonb_build_object('admin',coalesce(b2b_private.is_owner(),false));
end $$;
create or replace function public.hajeung_web_settings() returns jsonb language plpgsql stable security definer set search_path='' as $$
declare s jsonb; h jsonb;
begin
 perform b2b_private.verified_email();
 if not coalesce(b2b_private.is_owner(),false) then raise exception '기존 AP 관리자만 운영 설정을 볼 수 있습니다.' using errcode='42501';end if;
 s:=b2b_private.mail_state();if s is null then raise exception '메일 규칙을 불러오지 못했습니다.';end if;
 select coalesce(jsonb_agg(x order by x.at desc),'[]'::jsonb) into h from (
 select at,actor,detail->'after'->>'days' as days,detail->'after'->>'mode' as mode from hajeung.audit_log where action='웹 메일 설정 저장' order by at desc limit 20) x;
 return s||jsonb_build_object('revision',md5(s::text),'history',h);
end $$;
create or replace function public.hajeung_web_save(p jsonb) returns jsonb language plpgsql security definer set search_path='' as $$
<<input>>
declare actor text; old jsonb; fresh jsonb; days integer; recipient text; person text; mode text; subject text; body text; m text[];
begin
 actor:=b2b_private.verified_email();
 if not coalesce(b2b_private.is_owner(),false) then raise exception '기존 AP 관리자만 운영 설정을 변경할 수 있습니다.' using errcode='42501';end if;
 if jsonb_typeof(p->'days') is distinct from 'number' or coalesce(p->>'days','')!~'^[0-9]{1,3}$' then raise exception '발송 기준은 1~365일 정수로 입력해 주세요.';end if;
 days:=(p->>'days')::integer;if days<1 or days>365 then raise exception '발송 기준은 1~365일입니다.';end if;
 recipient:=trim(coalesce(p->>'recipient',''));person:=trim(coalesce(p->>'name',''));mode:=p->>'mode';subject:=trim(coalesce(p->>'subject',''));body:=trim(coalesce(p->>'body',''));
 if recipient='' or length(recipient)>500 or exists(select 1 from regexp_split_to_table(recipient,',') e where trim(e)!~'^[^@\s]+@[^@\s]+\.[^@\s]+$') then raise exception '수신 이메일을 확인해 주세요.';end if;
 if length(person)>100 or mode is null or mode not in ('자동','승인') or length(subject) not between 1 and 300 or length(body) not between 1 and 10000 then raise exception '이름·발송 방식·제목·본문을 확인해 주세요.';end if;
 for m in select regexp_matches(subject||body,'\{([^{}]+)\}','g') loop
 if m[1] not in ('수신자','담당자','업체','공사','현장','증권번호','발급기관','금액','종료일','D','비고','회신','발신부서','서명','기준일수','잔여일') then raise exception '지원하지 않는 문구 변수입니다: %',m[1];end if;
 end loop;
 if position('{기준일수}' in subject||body)=0 then raise exception '날짜와 문구가 일치하도록 제목이나 본문에 {기준일수}를 넣어 주세요.';end if;
 perform 1 from hajeung.settings where key in ('default_mail_to','default_mail_name','send_mode') order by key for update;
 perform 1 from hajeung.mail_rules where key in ('D60','D30','REMIND') order by key for update;
 old:=b2b_private.mail_state();if p->>'revision' is distinct from md5(old::text) then raise exception '다른 화면에서 설정이 변경됐습니다. 새로고침 후 다시 저장해 주세요.' using errcode='40001';end if;
 update hajeung.mail_rules set days=input.days,active=true,name=input.days::text||'일 이내 안내',subject=input.subject,body=input.body where key='D60';
 update hajeung.mail_rules set active=false where key in ('D30','REMIND');
 insert into hajeung.settings(key,value) values('default_mail_to',recipient),('default_mail_name',person),('send_mode',mode) on conflict(key) do update set value=excluded.value;
 fresh:=b2b_private.mail_state();insert into hajeung.audit_log(actor,action,detail) values(actor,'웹 메일 설정 저장',jsonb_build_object('before',old,'after',fresh));
 return public.hajeung_web_settings();
end $$;
revoke all on function public.hajeung_web_context(),public.hajeung_web_settings(),public.hajeung_web_save(jsonb) from public,anon;
grant execute on function public.hajeung_web_context(),public.hajeung_web_settings(),public.hajeung_web_save(jsonb) to authenticated;
commit;
