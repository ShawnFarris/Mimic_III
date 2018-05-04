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
    parser.add_argument("-code","--code", dest = 'code', type = str, action = 'store') 
    parser.set_defaults(code = '401')
    args = parser.parse_args()    
    
    return args

args = get_args()
print(args)
base = os.getcwd()

#### Load ICD decriptions
icd9_desc = pd.read_csv(base + '/ICD_Data/icd9_desc.csv')

#### Script Parameters
np.random.seed(12)

#### Load tsne data
df_tsne = pd.read_csv(base + '/Processed_Data/icd_tsne.csv')


#### Load embedding dict
with open(base + '/icd_embedding_dict.pickle', 'rb') as handle:
   embedding_dict = pickle.load(handle)

X = embedding_dict.get('embedding_matrix')
vocab = embedding_dict.get('vocab')
model = embedding_dict.get('model')


#### Most Similar Codes
def get_top_codes(code):
    top_words = pd.DataFrame(model.predict_output_word([code], topn = 10))
    top_words.rename(columns = {0:'icd9',1:'Distance'},inplace=True)
    top_words = pd.merge(top_words,icd9_desc,how='inner')
    
    target_word_desc = icd9_desc[icd9_desc['icd9'] == code]['description'].values[0]
    print('Most similar codes for ' + code + ' (' + target_word_desc + '): ')
    print(top_words)


get_top_codes(args.code)


