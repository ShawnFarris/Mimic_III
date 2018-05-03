#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: shawn
"""
from gensim.models import Word2Vec
import pickle
import pandas as pd
import numpy as np
import os
import pickle
from matplotlib import pyplot
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from ggplot import ggplot, geom_point, scale_color_manual, ggtitle, aes
from ggplot import *
from sklearn.cluster import KMeans
import sys
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
icd9_desc = pd.read_csv(base + '/icd9_desc.csv')

#### Script Parameters
np.random.seed(12)

#### Load tsne data
df_tsne = pd.read_csv(base + '/icd_tsne.csv')


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
        with open(base + '/icd_embedding_dict.pickle', 'rb') as handle:
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
   
plot_embedding(show_plot = args.show_plots)
plot_embedding(show_plot = args.show_plots, label = 'Category')
plot_embedding(show_plot = args.show_plots,label = 'Cluster')



##### Most Similar Codes
#def get_top_codes(code):
#    top_words = pd.DataFrame(model.predict_output_word([code], topn = 10))
#    top_words.rename(columns = {0:'icd9',1:'Distance'},inplace=True)
#    top_words = pd.merge(top_words,icd9_desc,how='inner')
#    
#    target_word_desc = icd9_desc[icd9_desc['icd9'] == code]['description'].values[0]
#    print('Most similar codes for ' + code + ' (' + target_word_desc + '): ')
#    print(top_words)
#
#
## hypertension: 401.9
#code = '401'
#get_top_codes('401')
#
#
#
## Diabetes
#get_top_codes('250')
#
#
#
#get_top_codes('950')
#
#
#get_top_codes('764')
#
#
#
################# interactive plots ############
#
#
#import plotly.plotly as py
#from plotly.graph_objs import *
#
#from plotly import __version__
#from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
#
#
#plot_df = df_tsne.copy(deep = True)
#plot_df = pd.merge(plot_df, icd9_desc, left_on = 'label', right_on = 'icd9',how='left')
#plot_df['category2'] = plot_df['range'].str[:] + ' ' + plot_df['category']
#
##    
##
##plot_df.drop('label',axis=1,inplace=True)
##
##trace1 = Scatter(
##    x=plot_df['x1'],
##    y=plot_df['x2']
##)
##
##data = Data([trace1])
##py.plot(data, filename = 'basic-line')
#
#
#from plotly.graph_objs import Scatter, Figure, Layout, Annotations, Annotation
#
#
##### layout creates dict
##layout = Layout(
##            annotations=Annotations([
##        Annotation(
##            x=plot_df['x1'].iloc[0],
##            y=plot_df['x2'].iloc[0],
##            showarrow=False,
##            text=plot_df['label'].iloc[0],
##            xref='x',
##            yref='y'
##        ),
##        Annotation(
##            x=plot_df['x1'].iloc[1],
##            y=plot_df['x2'].iloc[1],
##            showarrow=False,
##            text=plot_df['x1'].iloc[1],
##            textangle=-90,
##            xref='paper',
##            yref='paper'
##        )
##    ])
##)
##
##
####### create annotation_dict
##        
##inner_dict = layout.get('annotations') # this is an array 
##inner_dict[0] # this is a dict
##
#
#
#inner_array = []
#for i in range(plot_df.shape[0]):
#    
#    val = {
#    'showarrow':False, 
#    'arrowhead':1,
#    'text': plot_df['label'].iloc[i],
#    'x': plot_df['x1'].iloc[i],
#    'xref': 'x',
#    'y': plot_df['x2'].iloc[i]+0.2,
#    'yref': 'y'
##    'textangle':-90
#    }
#    inner_array.append(val)
#        
#layout = {'annotations':inner_array}
#
#
#
#data = [Scatter(x=plot_df['x1'], y=plot_df['x2'], 
#              mode = 'markers',              
#              marker=dict(size='5',                              
##                          color = np.random.randn(500), #set color equal to a variable
##                          colorscale='Viridis',
##                          showscale=True
#                            ),
#                          text = plot_df['category2'],
#                          textposition='top')
#    ]
#
#fig = Figure(data=data,layout=layout)
#
#plot(fig, auto_open = False)
#
##py.plot(fig, filename='code_embedding', auto_open = False)
##   
#
#
#
#
#
#
#
#
#
#
