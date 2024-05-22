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
df = pd.read_csv("news_classified_2021_2024_3.csv")
df["sentiment"].value_counts()
df["content"] = df["content"].astype(str)


# filter data for category of interest
#test = df[df["sentiment"] == "public policy and legislation"]
filter_list = ["safe injection sites", "needle exchange programs", "medication-assisted treatment", "opioid replacement", "prevention", "rehabilitation and recovery", "nalaxone", "funding opportunity", "decriminalization", "public policy and legislation"] 
# filter dataframe for only solutions and policy
dfq = df[df["sentiment"].isin(filter_list)]

dfq.columns
dfq["publishedAt"].dtype


dfq["year"] = dfq['publishedAt'].str[0:4]

dfq["year"].value_counts()
# get NER results
results = batch_6['content'].apply(lambda x: {x: get_ner_fx(final_prompt, x)})

# write to CSV
results.to_csv("ner_results_2021_2024_6.csv", index = False)

results


# for one result
funding = df[df["sentiment"] == "funding opportunity"]

result = get_ner_fx(final_prompt,funding["content"][74] )

result

funding.head(1)
funding.columns