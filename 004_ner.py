import openai
import os
from openai import AzureOpenAI

# get API key
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_key