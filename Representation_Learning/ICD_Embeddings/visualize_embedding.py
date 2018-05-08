#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: shawn
"""

import pickle
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from ggplot import ggplot, geom_point, scale_color_manual, ggtitle, aes
from ggplot import *
from sklearn.cluster import KMeans
import argparse

def get_args():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--show_plots", dest = 'show_plots', action = 'store_true')
 
    parser.set_defaults(show_plots = False)
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


#################### Plot Embeddings ##################
def plot_embedding(show_plot = False, label = '',  n_clusters = 5):
    
    plot_df = df_tsne.copy(deep = True)    
    if label == '':
        plt.figure(figsize = (12,8))
        plt.scatter(plot_df.iloc[:, 0], plot_df.iloc[:, 1])
        plt.title('ICD Code Embeddings')
        plt.savefig(base + '/Plots/icd_embedding.png')
        if show_plot:
            plt.show()       
            
    elif label == 'Category':
        ### Annotate by desc
        plot_df = df_tsne.copy(deep = True)
        plot_df = pd.merge(plot_df, icd9_desc, left_on = 'label', right_on = 'icd9',how='left')
        plot_df.drop(['label','icd9'],axis=1,inplace=True)
        plot_df.rename(columns = {'range':'label'},inplace=True)
                  
        chart = ggplot(plot_df, aes(x='x1', y='x2',color = 'label') ) \
                + geom_point(size=70
                             ,alpha=0.6
                             ) \
                + ggtitle("Word2Vec Embeddings")
#                + scale_color_manual(values = ["red", "blue","green", "purple","orange"
        #                                       , "#6DABE4","#65CBC9"
        
        chart.save(base + '/Plots/icd_embedding_categories.png')                
        if show_plot:               
            print(chart)

                               

    elif label == 'Cluster':

        #### Load embedding dict
        with open(base + '/Processed_Data/icd_embedding_dict.pickle', 'rb') as handle:
           embedding_dict = pickle.load(handle)
        
        X = embedding_dict.get('embedding_matrix')

        #### Cluster on Embedding Space 
        icd_clusters = KMeans(n_clusters = n_clusters, random_state = 1).fit(X)
        # Reorder Clusters
        idx = pd.DataFrame(icd_clusters.labels_)[0].value_counts().index.values
        lut = np.zeros_like(idx)
        lut[idx] = np.arange(n_clusters)
        plot_df['label'] = lut[icd_clusters.labels_].astype(str)

        chart = ggplot(plot_df, aes(x='x1', y='x2',color = 'label') ) \
            + geom_point(size=70
                         ,alpha=0.6
                         ) \
            + ggtitle("Word2Vec Embeddings")\
            + scale_color_manual(values = ["red", "blue","green", "purple","orange"
    #                                       , "#6DABE4","#65CBC9"
                                           ])
        chart.save(base + '/Plots/icd_clustered_embedding.png')                
        if show_plot:               
            print(chart)
            
    elif label == 'Code_type':      
        ### Annotate by desc
        plot_df = df_tsne.copy(deep = True)
        plot_df = pd.merge(plot_df, icd9_desc, left_on = 'label', right_on = 'icd9',how='left')
        plot_df.drop(['label','icd9'],axis=1,inplace=True)
        plot_df.rename(columns = {'type':'label'},inplace=True)
                  
        chart = ggplot(plot_df, aes(x='x1', y='x2',color = 'label') ) \
                + geom_point(size=70
                             ,alpha=0.6
                             ) \
                + ggtitle("Word2Vec Embeddings")
#                + scale_color_manual(values = ["red", "blue","green", "purple","orange"
        #                                       , "#6DABE4","#65CBC9"
        
        chart.save(base + '/Plots/icd_embedding_code_type.png')                
        if show_plot:               
            print(chart)
   
plot_embedding(show_plot = args.show_plots)
plot_embedding(show_plot = args.show_plots, label = 'Category')
plot_embedding(show_plot = args.show_plots,label = 'Cluster')
plot_embedding(show_plot = args.show_plots, label = 'Code_type')


