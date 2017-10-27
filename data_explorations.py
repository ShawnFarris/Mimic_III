#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 13:19:39 2017

@author: ShawnFarris
"""

# Import libraries
import os
import json
import numpy as np
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import datetime as dt
import glob


%matplotlib inline

# create a database connection
sqluser = 'postgres'
dbname = 'mimic'
schema_name = 'mimiciii'


# Specify List of Cookbook Queries from MIMIC Repo
query_path = '/Users/ShawnFarris/mimic-code/concepts/cookbook'
query_list = glob.glob(query_path + "/*.sql")
query_names = [query_list[i].split("/")[-1] for i in range(len(query_list))]



# Connect to local postgres version of mimic
con = psycopg2.connect(dbname=dbname, user=sqluser)
cur = con.cursor()
cur.execute('SET search_path to ' + schema_name)

# Read in desired query
def get_query(query_name):
    index = query_names.index(query_name + '.sql')
    with open(query_list[index],'r') as fp:
        query = fp.read()
    return query


query = get_query('age-histogram')

model_df = pd.read_sql_query(query,con)

model_df



