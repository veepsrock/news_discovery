import openai
import os
from openai import AzureOpenAI
import json
import importlib
import sys
import pandas as pd

# load functions
with open('project_config.json','r') as fp: 
    project_config = json.load(fp)
 
module_path = os.path.join(project_config['project_module_relative_path'])
sys.path.append(module_path)

import get_ner
importlib.reload(get_ner)
from get_ner import *

# read in data
df = pd.read_csv("brazil_news_filtered_2022_2024.csv")
df["sentiment"].value_counts()
df["content"] = df["content"].astype(str)


# filter data for category of interest
#test = df[df["sentiment"] == "public policy and legislation"]
filter_list = ["safe injection sites", "needle exchange programs", "medication-assisted treatment", "opioid replacement", "prevention", "rehabilitation and recovery", "nalaxone", "funding opportunity", "decriminalization", "public policy and legislation"] 
# filter dataframe for only solutions and policy
dfq = df[df["sentiment"].isin(filter_list)]
dfq["year"] = dfq['publishedAt'].str[0:4]
dfq.to_csv("news_filtered_categories.csv", index = False)
dfq.shape
# get NER results

results = dfq['content'].apply(lambda x: {x: get_ner_fx(final_prompt, x)})

# write to CSV
results.to_csv("brazil_ner_results_2021_2024_q_2.csv", index = False)

result = get_ner_fx(final_prompt, dfq["content"][6])

result