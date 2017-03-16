import os, re
import pandas as pd


## Load Index and vocabulary

print("Loading Index...\n")
ind = loadIndex()    # load index in memory
voc = loadVocabulary()    # load vocabulary in memory
X = (ind, voc)    # create ind,voc tuple
print("Index loaded.\n")

## SEARCH INTERFACE

print("Search : ",end = '')
query = str(input( ))    # input query

searchResults = search(query, *X)
docIDResults  = [d[0] for d in searchResults]

print("Found "+str(len(docIDResults))+ " results.\n")

max_results = 10    # set max number of result to output

results = cosSim(query, docIDResults, *X)[:max_results]
printResults(results)
