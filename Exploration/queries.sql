set search_path to mimiciii;


#### ICU Stay View Exploration ####
select * from icustay_detail limit 10;

select distinct subject_id, count(*) as cnt 
from icustay_detail
group by subject_id
order by cnt desc;

select * from icustay_detail where subject_id = 13033;


#### labs_agg
select * from lab_aggs limit 10;


#### Cookbook Scripts

# age-histogram
WITH agetbl AS
(
    SELECT (extract(DAY FROM ad.admittime - p.dob)
            + extract(HOUR FROM ad.admittime - p.dob) / 24
            + extract(MINUTE FROM ad.admittime - p.dob) / 24 / 60
            ) / 365.25
            AS age
      FROM admissions ad
      INNER JOIN patients p
      ON ad.subject_id = p.subject_id
)
, agebin AS
(
      SELECT age, width_bucket(age, 15, 100, 85) AS bucket
      FROM agetbl
)
SELECT bucket+15 as age, count(*)
FROM agebin
GROUP BY bucket
ORDER BY bucket;