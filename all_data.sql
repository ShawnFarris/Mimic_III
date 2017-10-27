drop materialized view if exists lab_aggs;
create materialized view lab_aggs as


    select le.subject_id, le.hadm_id

    , min(case when le.itemid=51006 then le.valuenum else null end) as urea_N_min

    , max(case when le.itemid=51006 then le.valuenum else null end) as urea_N_max

    , avg(case when le.itemid=51006 then le.valuenum else null end) as urea_N_mean

    , min(case when le.itemid=51265 then le.valuenum else null end) as platelets_min

    , max(case when le.itemid=51265 then le.valuenum else null end) as platelets_max

    , avg(case when le.itemid=51265 then le.valuenum else null end) as platelets_mean

    , max(case when le.itemid=50960 then le.valuenum else null end) as magnesium_max

    , min(case when le.itemid=50862 then le.valuenum else null end) as albumin_min

    , min(case when le.itemid=50893 then le.valuenum else null end) as calcium_min

    from labevents le

    where hadm_id is not null

    group by 1,2 order by 1,2

 
drop materialized view if exists chartevent_aggs;
create materialized view chartevent_aggs as

    select hadm_id

    , min(case when itemid in (615,618,220210,224690) and valuenum > 0 and valuenum < 70 then valuenum else null end) as RespRate_Min

    , max(case when itemid in (615,618,220210,224690) and valuenum > 0 and valuenum < 70 then valuenum else null end) as RespRate_Max

    , avg(case when itemid in (615,618,220210,224690) and valuenum > 0 and valuenum < 70 then valuenum else null end) as RespRate_Mean

    , min(case when itemid in (807,811,1529,3745,3744,225664,220621,226537) and valuenum > 0 then valuenum else null end) as Glucose_Min

    , max(case when itemid in (807,811,1529,3745,3744,225664,220621,226537) and valuenum > 0 then valuenum else null end) as Glucose_Max

    , avg(case when itemid in (807,811,1529,3745,3744,225664,220621,226537) and valuenum > 0 then valuenum else null end) as Glucose_Mean

    , min(case when itemid in (211,220045) and valuenum > 0 and valuenum < 300 then valuenum else null end) as HR_min

    , max(case when itemid in (211,220045) and valuenum > 0 and valuenum < 300 then valuenum else null end) as HR_max

    , round(cast(avg(case when itemid in (211,220045) and valuenum > 0 and valuenum < 300 then valuenum else null end) as numeric), 2) as HR_mean

    , min(case when itemid in (51,442,455,6701,220179,220050) and valuenum > 0 and valuenum < 400 then valuenum else null end) as SysBP_min

    , max(case when itemid in (51,442,455,6701,220179,220050) and valuenum > 0 and valuenum < 400 then valuenum else null end) as SysBP_max

    , round(cast(avg(case when itemid in (51,442,455,6701,220179,220050) and valuenum > 0 and valuenum < 400 then valuenum else null end) as numeric), 2) as SysBP_mean

    , min(case when itemid in (8368,8440,8441,8555,220180,220051) and valuenum > 0 and valuenum < 300 then valuenum else null end) as DiasBP_min

    , max(case when itemid in (8368,8440,8441,8555,220180,220051) and valuenum > 0 and valuenum < 300 then valuenum else null end) as DiasBP_max

    , round(cast(avg(case when itemid in (8368,8440,8441,8555,220180,220051) and valuenum > 0 and valuenum < 300 then valuenum else null end) as numeric), 2) as DiasBP_mean

    , min(case when itemid in (223761,678) and valuenum > 70 and valuenum < 120 then (valuenum-32)/1.8

               when itemid in (223762,676)  and valuenum > 10 and valuenum < 50 then valuenum else null end) as temp_min

    , max(case when itemid in (223761,678) and valuenum > 70 and valuenum < 120 then (valuenum-32)/1.8

               when itemid in (223762,676)  and valuenum > 10 and valuenum < 50 then valuenum else null end) as temp_max

    , round(cast(avg(case when itemid in (223761,678) and valuenum > 70 and valuenum < 120 then (valuenum-32)/1.8

               when itemid in (223762,676)  and valuenum > 10 and valuenum < 50 then valuenum else null end) as numeric), 2) as temp_mean

    from chartevents

    where itemid in

    (

      615,618,220210,224690, --- RespRate

      807,811,1529,3745,3744,225664,220621,226537, --- Glucose

      211,220045,---HR

      51,442,455,6701,220179,220050,---SysBP

      8368,8440,8441,8555,220180,220051,--DiasBP

      223761,678,223762,676--Temp

    )

    and hadm_id is not null

    group by 1

  
drop materialized view if exists output_agg;
create materialized view output_agg as

    select hadm_id

    , min(value) as urine_min

    , max(value) as urine_max

    , round(cast(avg(value) as numeric)) as urine_mean

    from outputevents

    where itemid in (40055,226559)

    and hadm_id is not null

    group by 1

  
