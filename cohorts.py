# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 14:47:31 2017

@author: shawn
"""

# Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2

# below imports are used to print out pretty pandas dataframes
from IPython.display import display, HTML

%matplotlib inline
plt.style.use('ggplot')

# information used to create a database connection
sqluser = 'postgres'
dbname = 'mimic'
schema_name = 'mimiciii'
password = 'password'

# Connect to postgres with a copy of the MIMIC-III database
con = psycopg2.connect(dbname=dbname, user=sqluser, password = password)

# the below statement is prepended to queries to ensure they select from the right schema
query_schema = 'set search_path to ' + schema_name + ';'

# Select Header for ICUStays
query = query_schema + """
SELECT subject_id, hadm_id, icustay_id
FROM icustays
LIMIT 10
"""
df = pd.read_sql_query(query, con)
df.head()

# Compute Stay Length for ICU stays in fractional days
query = query_schema + """
SELECT subject_id, hadm_id, icustay_id
, EXTRACT(EPOCH FROM outtime - intime)/60.0/60.0/24.0 as icu_length_of_stay
FROM icustays
LIMIT 10
"""
df = pd.read_sql_query(query, con)
df.head()

# Thus, we can filter to patients with minimum LOS's
query = query_schema + """
WITH co AS
(
SELECT subject_id, hadm_id, icustay_id
, EXTRACT(EPOCH FROM outtime - intime)/60.0/60.0/24.0 as icu_length_of_stay
FROM icustays
LIMIT 10
)
SELECT
  co.subject_id, co.hadm_id, co.icustay_id, co.icu_length_of_stay
FROM co
WHERE icu_length_of_stay >= 2
"""
df = pd.read_sql_query(query, con)
df


# Rep'n the above as a chort table with binary flags

query = query_schema + """
WITH co AS
(
SELECT subject_id, hadm_id, icustay_id
, EXTRACT(EPOCH FROM outtime - intime)/60.0/60.0/24.0 as icu_length_of_stay
FROM icustays
LIMIT 10
)
SELECT
  co.subject_id, co.hadm_id, co.icustay_id, co.icu_length_of_stay
  , CASE
        WHEN co.icu_length_of_stay < 2 then 1
    ELSE 0 END
        as exclusion_los
FROM co
"""
df = pd.read_sql_query(query, con)
df

# Computing Patiens Age
query = query_schema + """
WITH co AS
(
SELECT icu.subject_id, icu.hadm_id, icu.icustay_id
, EXTRACT(EPOCH FROM outtime - intime)/60.0/60.0/24.0 as icu_length_of_stay
, icu.intime - pat.dob AS age
FROM icustays icu
INNER JOIN patients pat
  ON icu.subject_id = pat.subject_id
LIMIT 10
)
SELECT
  co.subject_id, co.hadm_id, co.icustay_id, co.icu_length_of_stay
  , co.age
  , EXTRACT('year' FROM co.age) as age_extract_year 
  , EXTRACT('year' FROM co.age) 
    + EXTRACT('months' FROM co.age) / 12.0
    + EXTRACT('days' FROM co.age) / 365.242
    + EXTRACT('hours' FROM co.age) / 24.0 / 364.242
    as age_extract_precise
  , EXTRACT('epoch' from co.age) / 60.0 / 60.0 / 24.0 / 365.242 as age_extract_epoch
  , CASE
        WHEN co.icu_length_of_stay < 2 then 1
    ELSE 0 END
        as exclusion_los
FROM co
"""
df = pd.read_sql_query(query, con)
df

# Augment to filter to only include adults
query = query_schema + """
WITH co AS
(
SELECT icu.subject_id, icu.hadm_id, icu.icustay_id
, EXTRACT(EPOCH FROM outtime - intime)/60.0/60.0/24.0 as icu_length_of_stay
, EXTRACT('epoch' from icu.intime - pat.dob) / 60.0 / 60.0 / 24.0 / 365.242 as age
FROM icustays icu
INNER JOIN patients pat
  ON icu.subject_id = pat.subject_id
LIMIT 10
)
SELECT
  co.subject_id, co.hadm_id, co.icustay_id, co.icu_length_of_stay
  , co.age
  , CASE
        WHEN co.icu_length_of_stay < 2 then 1
    ELSE 0 END
        as exclusion_los
  , CASE
        WHEN co.age < 16 then 1
    ELSE 0 END
        as exclusion_age
FROM co
"""
df = pd.read_sql_query(query, con)
df


# Identifying patients with mutliple ICU stays
query = query_schema + """
WITH co AS
(
SELECT icu.subject_id, icu.hadm_id, icu.icustay_id
, EXTRACT(EPOCH FROM outtime - intime)/60.0/60.0/24.0 as icu_length_of_stay
, EXTRACT('epoch' from icu.intime - pat.dob) / 60.0 / 60.0 / 24.0 / 365.242 as age

, RANK() OVER (PARTITION BY icu.subject_id ORDER BY icu.intime) AS icustay_id_order

FROM icustays icu
INNER JOIN patients pat
  ON icu.subject_id = pat.subject_id
LIMIT 10
)
SELECT
  co.subject_id, co.hadm_id, co.icustay_id, co.icu_length_of_stay
  , co.age
  , co.icustay_id_order
  
  , CASE
        WHEN co.icu_length_of_stay < 2 then 1
    ELSE 0 END
        as exclusion_los
  , CASE
        WHEN co.age < 16 then 1
    ELSE 0 END
        as exclusion_age
FROM co
"""
df = pd.read_sql_query(query, con)
df

# Filter to include only patients FIRST ICU stay
query = query_schema + """
WITH co AS
(
SELECT icu.subject_id, icu.hadm_id, icu.icustay_id
, EXTRACT(EPOCH FROM outtime - intime)/60.0/60.0/24.0 as icu_length_of_stay
, EXTRACT('epoch' from icu.intime - pat.dob) / 60.0 / 60.0 / 24.0 / 365.242 as age

, RANK() OVER (PARTITION BY icu.subject_id ORDER BY icu.intime) AS icustay_id_order

FROM icustays icu
INNER JOIN patients pat
  ON icu.subject_id = pat.subject_id
LIMIT 10
)
SELECT
  co.subject_id, co.hadm_id, co.icustay_id, co.icu_length_of_stay
  , co.age
  , co.icustay_id_order
  
  , CASE
        WHEN co.icu_length_of_stay < 2 then 1
    ELSE 0 END
    AS exclusion_los
  , CASE
        WHEN co.age < 16 then 1
    ELSE 0 END
    AS exclusion_age
  , CASE 
        WHEN co.icustay_id_order != 1 THEN 1
    ELSE 0 END 
    AS exclusion_first_stay
FROM co
"""
df = pd.read_sql_query(query, con)
df


# s Service Condition
query = query_schema + """
SELECT subject_id, hadm_id, transfertime, prev_service, curr_service
FROM services
LIMIT 10
"""
df = pd.read_sql_query(query, con)
df

# Filtering to non-surgery patients
    # Note: Ortho surgery is given by 'ORTHO'
query = query_schema + """
SELECT hadm_id, curr_service
, CASE
    WHEN curr_service like '%SURG' then 1
    WHEN curr_service = 'ORTHO' then 1
    ELSE 0 END
  AS surgical
FROM services se
LIMIT 10
"""
df = pd.read_sql_query(query, con)
df

# Get ICU_stay_IDs from HADM_id

query = query_schema + """
SELECT icu.hadm_id, icu.icustay_id, curr_service
, CASE
    WHEN curr_service like '%SURG' then 1
    WHEN curr_service = 'ORTHO' then 1
    ELSE 0 END
  AS surgical
FROM icustays icu
LEFT JOIN services se
  ON icu.hadm_id = se.hadm_id
LIMIT 10
"""
df = pd.read_sql_query(query, con)
df


























