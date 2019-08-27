#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 17:43:30 2018

@author: shawn
"""

from gensim.models import Word2Vec
import pickle
import pandas as pd
import numpy as np
import os
import pickle
# from matplotlib import pyplot
# import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
# from ggplot import ggplot, geom_point, scale_color_manual, ggtitle, aes
# from ggplot import *
from sklearn.cluster import KMeans
import sys
import argparse

def get_args():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--pca_dimension", dest = 'pca_dimension', type = int)
    parser.add_argument("--tsne_perplexity", dest = 'tsne_perplexity', type = int)
    parser.add_argument("--tsne_iter", dest = 'tsne_iter', type = int)

    parser.set_defaults(pca_dimension = 10, tsne_perplexity = 40, 
                        tsne_iter = 300)
    args = parser.parse_args()    
    
    return args

args = get_args()
print(args)
base = os.getcwd()

#### Script Parameters
np.random.seed(12)

#### Load embedding dict
with open(base + '/Processed_Data/icd_embedding_dict.pickle', 'rb') as handle:
   embedding_dict = pickle.load(handle)

X = embedding_dict.get('embedding_matrix')
vocab = embedding_dict.get('vocab')
model = embedding_dict.get('model')
print('Embedding matrix dimension: ' + str(X.shape))



#### Reduce Dimension with PCA+TSNE
pca = PCA(n_components = args.pca_dimension, random_state = 12)
pca_result = pca.fit_transform(X)
df = pd.DataFrame(pca_result)

tsne = TSNE(n_components=2, verbose=1, perplexity = args.tsne_perplexity, n_iter= args.tsne_iter, random_state = 12)
tsne_results = tsne.fit_transform(df.values)

df_tsne = pd.DataFrame(tsne_results)
df_tsne.rename(columns = {0:'x1',1:'x2'}, inplace = True)
df_tsne['label'] = list(model.wv.vocab)

df_tsne.to_csv(base + '/Processed_Data/icd_tsne.csv',index = False)














