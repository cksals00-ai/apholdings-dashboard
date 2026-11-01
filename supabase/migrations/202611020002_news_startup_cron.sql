-- Independent of GitHub cron delivery and local computer availability.
select cron.schedule('ap-news-independent-kickoff','* 18-22 * * *',$job$
 select net.http_post(url := 'https://cgijpcimixaregbpvqbf.supabase.co/functions/v1/ap-news-kickoff', headers := jsonb_build_object('Authorization','Bearer ' || (select decrypted_secret from vault.decrypted_secrets where name='ap_news_scheduler'),'Content-Type','application/json'), body := '{}'::jsonb);
$job$);
