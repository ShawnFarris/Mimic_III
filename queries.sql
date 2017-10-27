set search_path to mimiciii;


#### ICU Stay View Exploration ####
select * from icustay_detail limit 10;

select distinct subject_id, count(*) as cnt 
from icustay_detail
group by subject_id
order by cnt desc;

select * from icustay_detail where subject_id = 13033;