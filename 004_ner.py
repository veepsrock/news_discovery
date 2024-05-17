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
df = pd.read_csv("news_classified.csv")
df["sentiment"].value_counts()

# filter data for category of interest
test = df[df["sentiment"] == "public policy and legislation"]

# get NER results
results = test['content'].apply(lambda x: {x: get_ner_fx(final_prompt, x)})

# write to CSV
results.to_csv("ner_results.csv", index = False)