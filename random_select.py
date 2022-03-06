#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 17:46:53 2022

@author: Kirsteenng
"""

import numpy as np
import pandas as pd
import json 
import random
import re

df = np.load('./longformer_all_review_predicted_score.npy')
test_path = './test_reviews.jsonl'


def parse_and_select(data:pd.DataFrame)->list:
    # each business ID has 10 reviews
    # each review consists of sentences of various lengths, 
    # need to parse these sentences and extract 50% by random
    random_select = []
    for i in range(0,len(data)):
        random_sentence = []
        full_review = ''
        full_review = ' '.join(data['reviews'][i])
        temp_sentence = re.sub('\n','',full_review)
        temp_sentence = re.sub(r'[.?!]+\s+', '<end>', temp_sentence)
        sentence_list = temp_sentence.split('<end>')
        random_sentence += random.sample(sentence_list,round(len(sentence_list)*0.3))
    
        random_select.append(random_sentence)
    return random_select
    

json_list = []
for line in open(test_path,'r'):
    json_list.append(json.loads(line))
    
data = pd.DataFrame(json_list)
data['random_sentence'] = parse_and_select(data)
data = data.drop(['reviews', 'scores','avg_score'],axis = 1)

data.to_csv('./test_reviews_with_random.csv')

    
    
    
