-- Rollback for 0001_optional_mirror.sql. Local canonical data is untouched.
select pgmq.drop_queue('alinacoder_optional_coordination');
drop table if exists public.alinacoder_memory_mirror;
