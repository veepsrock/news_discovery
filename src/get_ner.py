import openai
import os
from openai import AzureOpenAI


# connect to client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY_GPT4"),
    api_version="2023-12-01-preview",
    azure_endpoint= "https://rfaz-openai-gpt4.openai.azure.com"
)


SYSTEM_PROMPT = "You are a smart and intelligent Named Entity Recognition (NER) system. I will provide you the definition of the entities you need to extract, the sentence from where your extract the entities and the output format with examples."

USER_PROMPT_1 = "Are you clear about your role?"

ASSISTANT_PROMPT_1 = "Sure, I'm ready to help you with your NER task. Please provide me with the necessary information to get started."

GUIDELINES_PROMPT = (
    "Entity Definition:\n"
    "1. PERSON: Short name or full name of a person from any geographic regions.\n"
    "2. DATE: Any format of dates. Dates can also be in natural language.\n"
    "3. LOC: Name of any geographic location, like cities, countries, continents, districts etc.\n"
    "4. ORG: Name of any organizations, like companies, non-profits, ministries, etc.\n"
    "5. PROGRAMS: Name of any programs, activities, initiatives, campaigns, or pilots.\n"
    "\n"
    "Output Format:\n"
    "{{'PERSON': [list of entities present], 'DATE': [list of entities present], 'LOC': [list of entities present], 'ORG': [list of entities present], 'PROGRAMS': [list of entities present]}}\n"
    "If no entities are presented in any categories keep it None\n"
    "\n"
    "Examples:\n"
    "\n"
    "1. Sentence: Mr. Jacob lives in Madrid since 12th January 2015.\n"
    "Output: {{'PERSON': ['Mr. Jacob'], 'DATE': ['12th January 2015'], 'LOC': ['Madrid'], 'ORG': ['None'], 'PROGRAMS': ['None']}}\n"
    "\n"
    "2. Sentence: Mr. Rajeev Mishra and Sunita Roy are friends from Doctors Without Borders and they meet each other on 24/03/1998.\n"
    "Output: {{'PERSON': ['Mr. Rajeev Mishra', 'Sunita Roy'], 'DATE': ['24/03/1998'], 'LOC': ['None'], 'ORG': ['Doctors Without Borders'], 'PROGRAMS': ['None']}}\n"
    "\n"
    "3. Sentence: Vivian Peng implemented a new resource hub for safe injection sites in NY\n"
    "Output: {{'PERSON': ['Vivian Peng'], 'DATE': ['None'], 'LOC': ['NY'], 'ORG': ['None'], 'PROGRAMS': ['resource hub']}}\n"
)

final_prompt = GUIDELINES_PROMPT

# function to get ner
def get_ner_fx(final_prompt, sentence):
    final_prompt += f"\n\n3. Sentence: {sentence}\nOutput: "
    response = client.chat.completions.create(
        model="RFAZ-OpenAI-DataScience-ChatGPT4-32k", # This must match the custom deployment name you chose for your model.
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": USER_PROMPT_1},
                        {"role": "assistant", "content": ASSISTANT_PROMPT_1},
                        {"role": "user", "content": final_prompt}
                    ]
    )

    return response.choices[0].message.content.strip("\n")
