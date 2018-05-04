#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: shawn
"""
import pickle
import pandas as pd
import numpy as np
import os
import argparse

def get_args():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--show_distance", dest = 'show_show_distance', action = 'store_true')
    parser.add_argument("--show_desc", dest = 'show_show_desc', action = 'store_true')
    parser.set_defaults(show_distance = False, show_desc = False)
    args = parser.parse_args()    
    
    return args

args = get_args()
print(args)

base = os.getcwd()
pd.set_option('display.max_colwidth', 100)

#### Load ICD decriptions
icd9_desc = pd.read_csv(base + '/ICD_Data/icd9_desc.csv')

#### Script Parameters
np.random.seed(12)

#### Load embedding dict
with open(base + '/Processed_Data/icd_embedding_dict.pickle', 'rb') as handle:
   embedding_dict = pickle.load(handle)

X = embedding_dict.get('embedding_matrix')
vocab = embedding_dict.get('vocab')
model = embedding_dict.get('model')


#### Most Similar Codes
def get_top_codes(code):
    top_words = pd.DataFrame(model.predict_output_word([code], topn = 10))
    top_words.rename(columns = {0:'icd9',1:'Distance'},inplace=True)
    top_words = pd.merge(top_words,icd9_desc,how='inner')
    
    if args.show_distance == False:
        top_words.drop('Distance',axis=1,inplace=True)
        
    if args.show_desc == False:
        top_words.drop('description',axis=1,inplace=True)
    pd.options.display.max_colwidth          
    target_word_desc = icd9_desc[icd9_desc['icd9'] == code]['description'].values[0]
    print('\n')
    print('Most similar codes for ' + code + ' (' + target_word_desc + '): ')
    print('\n')
    print(top_words.to_string())
    


#options.display.max_colwidth

#### check if folder_path already saved
# To Do: eliminate need to rerun script
def get_code_similarity():
    stop_script = False
    while stop_script == False:        
        try:
            code = input("Input code or  'stop' to close script: ")
            if code[0] == code[-1] == "'" or code[0] == code[-1] == '"':
                code = code[1:-1]
           
            if code =='stop':
                stop_script = True
            else:
                get_top_codes(code)
                
        except pd.errors.MergeError:
            print('Invalid code.')

get_code_similarity()      

      
#        except FileNotFoundError:
#            mimic_data_path = input("Path to Mimic data not found. Enter path, unqouted: ")
#            if mimic_data_path[0] == mimic_data_path[-1] == "'" or mimic_data_path[0] == mimic_data_path[-1] == '"':
#                mimic_data_path = mimic_data_path[1:-1]
#                
#            folder_paths = {'mimic_data_path':mimic_data_path}
#            # Save in Seperate JSON
#            with open(os.getcwd() + '/folder_paths.json','w') as fp:
#                json.dump(folder_paths, fp)
#        








#get_top_codes(args.code)


