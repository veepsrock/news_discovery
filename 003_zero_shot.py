import pandas as pd
import re
import pickle
import numpy as np
from transformers import pipeline
classifier = pipeline("zero-shot-classification", model="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli")
import os
import sys
import json

# load functions
with open('project_config.json','r') as fp: 
    project_config = json.load(fp)
 
module_path = os.path.join(project_config['project_module_relative_path'])
sys.path.append(module_path)
 
import importlib
import zero_shot
importlib.reload(zero_shot)

from zero_shot import *


# read in data
df = pickle.load(open("news_filtered_2021_2024.pkl", "rb"))
df.shape

# make sure description column is reading as string
df['description'] = df['description'].astype(str)


# list of labels 
text_labels = ["medical malpractice", "lawsuit and settlement", "drug trafficking", "decriminalization", "public policy and legislation", "drug use disorder", "stigma", "addiction crisis", "overdose", "safe injection sites", "needle exchange programs", "medication-assisted treatment", "opioid replacement", "prevention", "rehabilitation and recovery", "nalaxone", "funding opportunity", "pharameutical industry"] 
# run prediction on df
results_list = []
if len(df) > 25:
    i = 0
    while i < len(df):
        batch = df.iloc[i:i+25, ]
        results_ = predict_sentiment(df=batch, text_column ="description", text_labels= text_labels)
        results_list.append(results_)
        i += 25
else:
    results_list.append(predict_sentiment(df=df, text_column ="description", text_labels= text_labels))

# conctenate results into final dataframe
results_df = pd.concat(results_list, ignore_index = True)  
results_df.shape
results_df.head()

# write to csv
results_df.to_csv("news_classified_2021_2024_3.csv", index = False)