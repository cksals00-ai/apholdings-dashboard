import{test}from'node:test';import assert from'node:assert/strict';import{readFile}from'node:fs/promises';import{PGlite}from'../../hajeung-server-safe/node_modules/@electric-sql/pglite/dist/index.js';
test('unconfirmed email cannot apply; existing operating identity cannot be overwritten',async()=>{
const db=new PGlite();await db.exec(`create role anon;create role authenticated;create schema auth;create schema storage;create schema hajeung;
create table auth.users(id uuid primary key,email text,email_confirmed_at timestamptz);create function auth.uid() returns uuid language sql stable as $$select nullif(current_setting('test.uid',true),'')::uuid$$;
create table storage.buckets(id text primary key,name text,public boolean,file_size_limit bigint,allowed_mime_types text[]);create table storage.objects(bucket_id text,name text);
create table hajeung.members(id uuid default gen_random_uuid(),email text unique,name text,role text,active boolean,demo boolean,code_hash text,code_issued_at timestamptz);
insert into auth.users values('11111111-1111-4111-8111-111111111111','existing@example.test',null),('94f18e51-cc1e-46c5-b2e0-235bf9221761','cksals00@gmail.com',now());`);
await db.exec(await readFile(new URL('../supabase/hajeung_support.sql',import.meta.url),'utf8'));
await db.exec("select set_config('test.uid','11111111-1111-4111-8111-111111111111',false);set role authenticated");await assert.rejects(db.query("select public.b2b_apply('테스트','테스트 회사','ios')"));
await db.exec("reset role;update auth.users set email_confirmed_at=now();insert into hajeung.members(email,name,role,active,demo,code_hash) values('existing@example.test','운영 담당자','관리자',true,false,'original');set role authenticated");
const id=(await db.query("select public.b2b_apply('테스트','테스트 회사','ios') as id")).rows[0].id;
await db.exec("reset role;select set_config('test.uid','94f18e51-cc1e-46c5-b2e0-235bf9221761',false);set role authenticated");await db.query("select public.b2b_application_status($1,'approved')",[id]);await assert.rejects(db.query('select public.b2b_issue_code($1)',[id]));
await db.exec('reset role');const m=(await db.query('select * from hajeung.members')).rows[0];assert.equal(m.demo,false);assert.equal(m.role,'관리자');assert.equal(m.code_hash,'original');await db.close();
});
