
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


'''
Notes:
    1. stemmed dx codes are only 2 digits (is this always true??)
        - options:
            1. process dx and px seperately
            2. adjust logic by including code source: dx or px in full_codes
    
'''

'''
Delete This

'''
#base = '/home/shawn/Mimic_III_dev/Full_ICD_Embeddings'
#args.truncate_codes = True
#args.min_sequence_length = 3

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
        
def load_data(data): 
        
    data_loaded = False
    # Check if MIMIC_Data path has already been saved
    with open(base + '/folder_paths.json') as fp:
        folder_paths = json.load(fp)
        
    while data_loaded == False:
        try:	
            df = pd.read_csv(folder_paths.get('mimic_data_path') + '/' + data + '_ICD.csv')
            print(data + ' data loaded.')
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
                
    return df

get_mimic_data_path()
diags = load_data(data='DIAGNOSES')
procedures = load_data(data='PROCEDURES')



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

# Truncate/stem codes
if args.truncate_codes:
    diags['ICD9_CODE'] = diags['ICD9_CODE'].str[0:3]
    procedures['ICD9_CODE'] = procedures['ICD9_CODE'].astype('str').str[0:2]


full_codes = pd.concat((diags,procedures),axis=0,ignore_index=True)


# drop: row_id, seq_num
full_codes.drop(['ROW_ID','SEQ_NUM'],axis=1,inplace=True)

# Drop Rows with blank codes
full_codes = full_codes.dropna()


########################################################################################################################
######################################             Visit Level Processing       ########################################
########################################################################################################################

# Create dataframe of ICD sequences
code_seqs = full_codes.groupby(['SUBJECT_ID','HADM_ID']).agg({'ICD9_CODE':concat_func}).reset_index()

# Shuffle sequences and drop duplicate codes
code_seqs['tmp'] = code_seqs['ICD9_CODE'].str.split(' ')
code_seqs['tmp'] = code_seqs['tmp'].apply(lambda x: shuffle_list(x))    
code_seqs['tmp'] = code_seqs['tmp'].apply(lambda x: remove_duplicates(x))    
code_seqs['ICD_SEQ'] = code_seqs['tmp'].apply(lambda x: ' '.join(x))
code_seqs.drop(['tmp','ICD9_CODE'],axis=1,inplace=True)


# Limit to sequences of given length
code_seqs['SEQ_LEN'] = code_seqs['ICD_SEQ'].str.split(' ').apply(lambda x: len(x))
code_seqs = code_seqs[code_seqs['SEQ_LEN'] >= args.min_sequence_length]
code_seqs.drop(['SEQ_LEN'], axis = 1, inplace = True)
    
# Save data in Model/embedding folder
code_seqs.to_csv(base + '/Processed_Data/icd_sequences.csv',index=False)
print('Processed sequences saved to: ' + base + '/Processed_Data/icd_sequences.csv')


