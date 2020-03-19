import pandas as pd
import nltk
from nltk.corpus import stopwords 
stopwords = stopwords.words('english')
import re
from collections import OrderedDict
import numpy as np
import os, sys
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import json


# input_loc = sys.argv[1]
# output_loc = sys.argv[2]
# stop_word_loc = sys.argv[3]
stop_word_loc = './stopwords.txt'

### Extract keyphrase for a sentence ###
def keyphrase_sentence(sentence): 
    sentence_re = r'''(?x)          
      (?:[A-Z]\.)+             
    | \w+(?:-\w+)*        
    | \$?\d+(?:\.\d+)?%?
    | \.\.\.              
    | [][.,;"'?():_`-]    
    '''
  
    toks = nltk.regexp_tokenize(sentence.lower(), sentence_re)  # sentence tokenisation

    postoks = nltk.tag.pos_tag(toks)

    for i in range(len(postoks)):
        if postoks[i][1][0]=='N'or postoks[i][1]=='RB' or postoks[i][1]=='DT':  # check if 'N'/'RB'/'DT' is appearing in pos list.
            token_ls = toks[i: len(toks)]        ## span of keyphrase ( starting point - 'N'/'RB'/'DT', 
                                                   ## ending point - ending of that sentence ) 
            token_ls = [i for i in token_ls if i not in stop_word_ls]  # remove stopwords from phrases.
            if len(token_ls)>=3:
                return " ".join(token_ls) 

### Extract keyphrase for a text ###
def keyphrase_text(text):
    
    phrase_ls = [ keyphrase_sentence(i) for i in text.split(". ") ] # extract keyphrases for each sentence in a text
    ls = {} 
    ls["Text"] = text
    ls["keyPhraseResults"] =[]
    for i in range(len(phrase_ls)): 
        try: 
            output = {} 
            sent = TextBlob(phrase_ls[i], analyzer = NaiveBayesAnalyzer()) # sentiment analysis on extracted keyphrases 
            output["keyphrase"] = phrase_ls[i]
            output["classification"] = sent.sentiment.classification
            output["pos_score"] = sent.sentiment.p_pos
            output["neg_score"] = sent.sentiment.p_neg
        except:
            print(i) 
        ls["keyPhraseResults"].append(output) 
    return ls 

with open(stop_word_loc) as f:                             # read stopword list
    stop_word_ls = [line.rstrip() for line in f] 

""" df = pd.read_csv(input_loc)                                  # read input text from a data frame   ####
results = {} 
results = {"output":[]}   
for i in range(len(df)): 
    data= keyphrase_text(df["Text"][i])
    results["output"].append(data) 

with open(output_loc, 'w') as f:
    json.dump(results, f)
 """

