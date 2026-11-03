-- Independent minute checks cover KST02:40–07:59; kickoff itself gates02:45–07:00.
select cron.schedule('ap-news-independent-kickoff','40-59 17 * * *',$job$
 select net.http_post(url := 'https://cgijpcimixaregbpvqbf.supabase.co/functions/v1/ap-news-kickoff', headers := jsonb_build_object('Authorization','Bearer ' || (select decrypted_secret from vault.decrypted_secrets where name='ap_news_scheduler'),'Content-Type','application/json'), body := '{}'::jsonb);
$job$);
select cron.schedule('ap-news-independent-kickoff-main','* 18-22 * * *',$job$
 select net.http_post(url := 'https://cgijpcimixaregbpvqbf.supabase.co/functions/v1/ap-news-kickoff', headers := jsonb_build_object('Authorization','Bearer ' || (select decrypted_secret from vault.decrypted_secrets where name='ap_news_scheduler'),'Content-Type','application/json'), body := '{}'::jsonb);
$job$);
