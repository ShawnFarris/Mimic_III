# Create ICD9 Code Embeddings for use in Machine Learning Algorthims

Navigate to the `ICD_Embeddings` folder from the terminal. When you are running these scripts for the first time, you will need to enter the path to your local copy of the Mimic III data as csv's. 

Start by loading the `diagnoses` data and processing it for embeddings:

```
python process_diagnoses.py < --full_codes, --min_sequences>
```

Compute train the Word2Vec embeddings of the diagnoses sequences:

```
python icd_embedding.py < --epochs, --embed_dim, 
                          --min_word_count, --workers, 
                          --down_sample, --window_size> 
```

The ICD code embeddings with be high dimensional, so to visualize the embeddings, we need to reduce the dimensionality:

```
python reduce_embedding_dimension.py <--pca_dimension,--tsne_perplexity,
                                      --tsne_iter>
```

We can view the embeddings:
```
python visualize_embeddings.py <--show_plots>
```

We can also explore code similarity under this embedding

```
python code_similarity.py <--code>
```
