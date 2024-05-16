import requests
import pandas as pd
import re
import os

# get newsapi key
news_key = os.getenv("NEWS_API_KEY")

# function to get news
def fetch_articles(page, keywords, start_date, end_date):
    url = "https://newsapi.org/v2/everything"
    api_key = news_key
    params = {
        "q" : keywords,
        "apiKey" : api_key, 
        "page": page,
        "from": start_date,
        "to": end_date,
        "language": 'en',
        "sort_by":'relevancy'
    }
    response = requests.get(url, params = params)
    return response

# unpack source into its own column
def create_dict(row_dict):
    dict = {
        'id' : row_dict['source']['id'],
        'source_name' : row_dict['source']['name']
    }
    return dict