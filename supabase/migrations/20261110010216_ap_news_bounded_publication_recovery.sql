-- Server recovery lease and bounded budget, separate from mail receipts.
create table public.ap_news_publication_recovery (
 issue_date date primary key, attempts integer not null default 0 check (attempts between 0 and 3),
 state text not null default 'idle', updated_at timestamptz not null default now()
);
alter table public.ap_news_publication_recovery enable row level security;
revoke all on public.ap_news_publication_recovery from anon, authenticated;
grant select,insert,update on public.ap_news_publication_recovery to service_role;
create function public.ap_news_publication_recovery_claim(p_day date) returns boolean
language plpgsql set search_path=public as $$
begin
 if p_day<>(now() at time zone 'Asia/Seoul')::date then raise exception 'Recovery must be today'; end if;
 insert into ap_news_publication_recovery(issue_date) values(p_day) on conflict do nothing;
 update ap_news_publication_recovery set attempts=attempts+1,state='requested',updated_at=now()
 where issue_date=p_day and attempts<3 and (attempts=0 or updated_at<now()-interval '2 minutes');
 return found;
end; $$;
revoke all on function public.ap_news_publication_recovery_claim(date) from public,anon,authenticated;
grant execute on function public.ap_news_publication_recovery_claim(date) to service_role;
