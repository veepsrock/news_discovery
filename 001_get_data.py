import requests
import pandas as pd
import re
import json
import os
import sys
import importlib
import query_news
importlib.reload(query_news)

# load functions
with open('project_config.json','r') as fp: 
    project_config = json.load(fp)
 
module_path = os.path.join(project_config['project_module_relative_path'])
sys.path.append(module_path)
 
from query_news import *


# get initial pull of results
page = 1
keywords = "opioids reduce prevention"
start_date = '2024-01-01'
end_date = '2024-05-16'
response = fetch_articles(page, keywords, start_date, end_date )
articles = response.json()["articles"] 
print("Total Results:", response.json()["totalResults"])

# loop through to get remaining pages
while len(articles) < response.json()["totalResults"]:
    page+=1
    response = fetch_articles(page, keywords, start_date, end_date)
    articles.extend(response.json()["articles"])
    print("Total Results:", response.json()["totalResults"], "Articles Pulled:", len(articles))


# create dataframe 
all_articles = []
for item in articles:
    source_dict = create_dict(item)
    all_articles.append({**item, **source_dict})
    
df = pd.DataFrame(all_articles)
df.drop("source", axis = 1, inplace = True)

# drop removed articles, or duplicates
# remove removed files
df = df[df["description"]!="[Removed]"]
df.drop_duplicates(subset=['author', 'title', 'url'], keep='first', inplace = True)

# write to csv
file_name = "_".join(keywords.split())
file_name = "_".join([file_name, start_date, end_date, ".csv"])
df.to_csv(file_name, index = False)


