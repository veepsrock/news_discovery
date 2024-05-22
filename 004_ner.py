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
df = pd.read_csv("news_classified_2021_2024.csv")
df["sentiment"].value_counts()
df["content"] = df["content"].astype(str)
df.shape

# filter data for category of interest
#test = df[df["sentiment"] == "public policy and legislation"]
batch_6 = df.iloc[200:253, ]
batch_6.shape
# get NER results
results = batch_6['content'].apply(lambda x: {x: get_ner_fx(final_prompt, x)})

# write to CSV
results.to_csv("ner_results_2021_2024_6.csv", index = False)

results