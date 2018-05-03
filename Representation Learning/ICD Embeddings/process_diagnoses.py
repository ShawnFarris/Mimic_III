
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 11:25:40 2018

@author: shawn
"""

import pandas as pd
import numpy as np
import sys
import pickle
from datetime import datetime
import os
import random
import sys


#### Get path to repo
# get repo path
file_name = "icd_processing.py"

# check os
if sys.platform == 'linux':
    start_point = r"/home"
elif sys.platform == 'darwin': # check this
    start_point = r"/Users"

for root, dirs, files in os.walk(start_point):
    for name in files:
        if name == file_name:
            script_path = os.path.abspath(root)
            print(script_path)
                        
base = script_path[0:script_path.find('Mimic_III_dev')+len('Mimic_III_dev')]


base = os.getcwd()





#### Load MIMIC III Diagnoses Data
mimic_data_folder_path = '/media/shawn/HDD/MIMIC_Data'
diags = pd.read_csv(mimic_data_folder_path + '/DIAGNOSES_ICD.csv')

# Data Parameters
truncate_codes = True
seq_len = 3

def concat_func(x):
        x = ' '.join(x.values)
        return x
      
def shuffle_list(x):
    x = random.sample(x, len(x))
    return x

# note this does not perserve order; still need to shuffle?
def remove_duplicates(x):
    return list(set(x))

#### Cols
    # subject_id = pat_id
    # hadm_id = hospital stay
    # seq_num = prioirty of code; SEQ_NUM == 1.0 ==> primiary_dx


# drop: row_id, seq_num
diags.drop(['ROW_ID','SEQ_NUM'],axis=1,inplace=True)

# Drop Rows with blank codes
diags = diags.dropna()

# Truncate/stem codes
if truncate_codes:
    diags['ICD9_CODE'] = diags['ICD9_CODE'].str[0:3]



#######################################################################################################################
#####################################             Visit Level Processing       ########################################
#######################################################################################################################

# Create dataframe of ICD sequences
diag_seqs = diags.groupby(['SUBJECT_ID','HADM_ID']).agg({'ICD9_CODE':concat_func}).reset_index()

# Shuffle sequences and drop duplicate codes
diag_seqs['tmp'] = diag_seqs['ICD9_CODE'].str.split(' ')
diag_seqs['tmp'] = diag_seqs['tmp'].apply(lambda x: shuffle_list(x))    
diag_seqs['tmp'] = diag_seqs['tmp'].apply(lambda x: remove_duplicates(x))    
diag_seqs['ICD_SEQ'] = diag_seqs['tmp'].apply(lambda x: ' '.join(x))
diag_seqs.drop(['tmp','ICD9_CODE'],axis=1,inplace=True)


# Limit to sequences of given length
diag_seqs['SEQ_LEN'] = diag_seqs['ICD_SEQ'].str.split(' ').apply(lambda x: len(x))
diag_seqs = diag_seqs[diag_seqs['SEQ_LEN'] >= seq_len]
diag_seqs.drop(['SEQ_LEN'], axis = 1, inplace = True)
    

# Save data in Model/embedding folder
diag_seqs.to_csv(base + '/Processed_Data/diagnoses_sequences.csv',index=False)


#######################################################################################################################
#####################################             Patient Level Processing     ########################################
#######################################################################################################################

#### To-do
# Issue: Do not have time indicators? Can get at stay level and have to convert to realtive indexes

diag_seqs.sort_values(['SUBJECT_ID','HADM_ID']).head()

