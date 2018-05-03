#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 10:53:26 2017

@author: ShawnFarris
"""

# Import libraries
import numpy as np
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

%matplotlib inline


# create a database connection
sqluser = 'postgres'
dbname = 'mimic'
schema_name = 'mimiciii'

# Connect to local postgres version of mimic
con = psycopg2.connect(dbname=dbname, user=sqluser)
cur = con.cursor()

#### Generate Aggregated Tables

# Model_DF
query = """ select la.subject_id, la.hadm_id, ad.admittime, ad.dischtime, ad.deathtime
  , ie.first_careunit, ie.last_careunit
  , extract(epoch from (ad.admittime - p.dob))/60.0/60.0/24.0/365.242 as age
  , p.gender as gender
  , ad.marital_status as marital_status
  , ad.insurance as insurance
  , urea_N_min
  , urea_N_max
  , urea_N_mean
  , platelets_min
  , platelets_max
  , platelets_mean
  , magnesium_max
  , albumin_min
  , calcium_min
  , RespRate_Min
  , RespRate_Max
  , RespRate_Mean
  , Glucose_Min
  , Glucose_Max
  , Glucose_Mean
  , HR_min
  , HR_max
  , HR_mean
  , SysBP_min
  , SysBP_max
  , SysBP_mean
  , DiasBP_min
  , DiasBP_max
  , DiasBP_mean
  , temp_min
  , temp_max
  , temp_mean
  , sapsii
  , sofa
  , urine_min
  , urine_mean
  , urine_max

  from lab_aggs la
    inner join output_agg oa
    on la.hadm_id = oa.hadm_id
    inner join patients p
    on la.subject_id = p.subject_id
    inner join admissions ad
    on la.hadm_id = ad.hadm_id
    inner join chartevent_aggs ca
    on la.hadm_id = ca.hadm_id
    inner join icustays ie
    on la.hadm_id = ie.hadm_id
    inner join SAPSII
    on la.hadm_id = SAPSII.hadm_id
    inner join SOFA
    on la.hadm_id = SOFA.hadm_id
  group by 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26
  ,27,28,29,30,31,32,33,34,35,36,37,38,39,40, 41, 42, 43
  order by 1,3
  ;"""
  
cur.execute('SET search_path to ' + schema_name)
model_df = pd.read_sql_query(query,con)
           

model_df.head()
model_df.shape

######################################################################################################################
###########################################            Explore Data              #####################################
######################################################################################################################


model_df.describe()

data = model_df.copy(deep = True)

#### Data Missingness
np.sum(data.isnull())/data.shape[0]

# Extract Readmission Time
# calculate time delta between subsequent readmissions of the same patient 
data['readmit_dt'] = np.zeros(data.shape[0])
data['next_readmit_dt'] = np.zeros(data.shape[0])
data['readmit_last_careunit'] = None

for idx in np.arange(1,data.shape[0]):
    if data.subject_id[idx] == data.subject_id[idx - 1]:     
        prev_disch = data.dischtime[idx-1]
        curr_adm = data.admittime[idx]
        dt = curr_adm - prev_disch
        dt_hrs_calc = np.round(dt.value/3600.0/1e9,2)

#         data.set_value(idx,'adm_num',data['adm_num'][idx-1] + 1) 
        data.set_value(idx,'readmit_dt',dt_hrs_calc)
        data.set_value(idx-1,'next_readmit_dt',dt_hrs_calc)
        data.set_value(idx,'readmit_last_careunit',data['last_careunit'][idx-1])





























    
    