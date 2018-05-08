#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: shawn
"""
import gensim
from gensim.models import Word2Vec
import pickle
import pandas as pd
import numpy as np
import os
import pickle
import argparse
import time
import sys

def get_args():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", dest = 'epochs', type = int)
    parser.add_argument("--embed_dim", dest = 'embed_dim', type = int)
    parser.add_argument("--min_word_count", dest = 'min_word_count', type = int)
    parser.add_argument("--workers", dest = 'workers', type = int)
    parser.add_argument("--down_sample", dest = 'down_sample', type = int)
    parser.add_argument("--window_size", dest = 'window_size', type = int)

    parser.set_defaults(epochs = 50, embed_dim = 100, 
                        min_word_count = 1, workers = 1, 
                        down_sample = 0,window_size = 5)
    args = parser.parse_args()    
    
    return args

args = get_args()
print(args)
base = os.getcwd()

#### Load diagnoses sequences
print('Loaded icd sequences.')
input_df = pd.read_csv(base + '/Processed_Data/icd_sequences.csv')

sents = input_df.drop(['SUBJECT_ID','HADM_ID'],axis=1)
sents = sents['ICD_SEQ'].str.split(' ')


# Note: Full reproducibility can't be had with multi-threading (I.E. workers > 1)
print('Training embedding.')
model = Word2Vec(sents, min_count = args.min_word_count, size = args.embed_dim, 
                 window = args.window_size, seed = 123, negative = 5, iter = args.epochs,
                 workers = args.workers, hs = 0, sample = args.down_sample,
                 sg = 1
                 )
X = model[model.wv.vocab]


#### Save
embedding_matrix = X
embedding_dict = {'embedding_matrix':embedding_matrix, 'model':model, 'vocab':model.wv.vocab}


with open(base + '/Processed_Data/icd_embedding_dict.pickle', 'wb') as handle:
    pickle.dump(embedding_dict , handle, protocol=pickle.HIGHEST_PROTOCOL)
print('Embedding dictionary saved to: ' + base + '/Processed_Data/icd_embedding_dict.pickle')





