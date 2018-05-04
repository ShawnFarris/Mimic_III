
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 11:25:40 2018

@author: shawn
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import random
import json
import argparse

def get_args():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--full_codes", dest = 'truncate_codes', action = 'store_false')
    parser.add_argument("--min_sequence_length", dest = 'min_sequence_length', type = int)
    parser.set_defaults(truncate_codes = True, min_sequence_length = 3)
    args = parser.parse_args()
    
    return args

args = get_args()
print(args)

# Get directory
base = os.getcwd()

#### check if folder_path already saved
# To Do: eliminate need to rerun script
def get_mimic_data_path():
    path_found = False
    while path_found == False:        
        try:
            # Check if MIMIC_Data path has already been saved
            with open(base + '/folder_paths.json') as fp:
                folder_paths = json.load(fp)
                print('Path to Mimic data found.')
            path_found = True 
            
        except FileNotFoundError:
            mimic_data_path = input("Path to Mimic data not found. Enter path, unqouted: ")
            if mimic_data_path[0] == mimic_data_path[-1] == "'" or mimic_data_path[0] == mimic_data_path[-1] == '"':
                mimic_data_path = mimic_data_path[1:-1]
                
            folder_paths = {'mimic_data_path':mimic_data_path}
            # Save in Seperate JSON
            with open(os.getcwd() + '/folder_paths.json','w') as fp:
                json.dump(folder_paths, fp)
        
def load_diagnoses_data(): 
    data_loaded = False
    # Check if MIMIC_Data path has already been saved
    with open(base + '/folder_paths.json') as fp:
        folder_paths = json.load(fp)
        
    while data_loaded == False:
        try:	
            diags = pd.read_csv(folder_paths.get('mimic_data_path') + '/DIAGNOSES_ICD.csv')
            print('Diagnoses data loaded.')
            data_loaded = True
            
        ## if mimic_data_path doesn't work            
        except FileNotFoundError:
            print('Mimic data not found. Reenter path to data.')
            mimic_data_path = input("Enter path to Mimic data, unqouted: ")
            if mimic_data_path[0] == mimic_data_path[-1] == "'" or mimic_data_path[0] == mimic_data_path[-1] == '"':
                mimic_data_path = mimic_data_path[1:-1]
        
            folder_paths = {'mimic_data_path':mimic_data_path}
            # Save in Seperate JSON
            with open(os.getcwd() + '/folder_paths.json','w') as fp:
                json.dump(folder_paths, fp)
                
    return diags

get_mimic_data_path()
diags = load_diagnoses_data()


##### Functions for sequence processing
def concat_func(x):
        x = ' '.join(x.values)
        return x
      
def shuffle_list(x):
    x = random.sample(x, len(x))
    return x

# note this does not perserve order
def remove_duplicates(x):
    return list(set(x))


# drop: row_id, seq_num
diags.drop(['ROW_ID','SEQ_NUM'],axis=1,inplace=True)

# Drop Rows with blank codes
diags = diags.dropna()

# Truncate/stem codes
if args.truncate_codes:
    diags['ICD9_CODE'] = diags['ICD9_CODE'].str[0:3]
    
########################################################################################################################
######################################             Visit Level Processing       ########################################
########################################################################################################################

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
diag_seqs = diag_seqs[diag_seqs['SEQ_LEN'] >= args.min_sequence_length]
diag_seqs.drop(['SEQ_LEN'], axis = 1, inplace = True)
    
# Save data in Model/embedding folder
diag_seqs.to_csv(base + '/diagnoses_sequences.csv',index=False)
print('Processed sequences saved to: ' + base + '/Processed_Data/diagnoses_sequences.csv')


