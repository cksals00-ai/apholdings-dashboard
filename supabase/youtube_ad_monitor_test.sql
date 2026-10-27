-- Execute with the project SQL editor as postgres. All changes roll back.
begin;
do $$
declare owner_id uuid; owner_count integer; other_count integer;
begin
  select user_id into owner_id from private.admin_portal_owners limit 1;
  if owner_id is null then raise exception 'Existing portal owner missing'; end if;
  perform set_config('request.jwt.claims', json_build_object('sub',owner_id,'role','authenticated')::text,true);
  execute 'set local role authenticated';
  select count(*) into owner_count from public.admin_youtube_ad_observations;
  execute 'reset role';
  perform set_config('request.jwt.claims','{"sub":"00000000-0000-0000-0000-000000000001","role":"authenticated"}',true);
  execute 'set local role authenticated';
  select count(*) into other_count from public.admin_youtube_ad_observations;
  execute 'reset role';
  if owner_count < 1 or other_count <> 0 then raise exception 'Owner isolation failed'; end if;
  if has_table_privilege('anon','public.admin_youtube_ad_observations','SELECT') or has_table_privilege('anon','public.admin_youtube_ad_api_checks','SELECT') then raise exception 'Anonymous read grant'; end if;
  if has_table_privilege('authenticated','public.admin_youtube_ad_observations','INSERT') or has_table_privilege('authenticated','public.admin_youtube_ad_api_checks','INSERT') then raise exception 'Unexpected browser write grant'; end if;
  begin
    insert into public.admin_youtube_ad_observations(promotion_id,observed_at,succeeded,views) values('1',now(),false,0);
    raise exception 'Failed observation accepted fabricated metric';
  exception when check_violation then null;
  end;
end $$;
rollback;
select 'PASS: owner reads, other user isolated, anon denied, browser writes denied, failed-check metric guard enforced' as verification;
