import openai
import os
from openai import AzureOpenAI
import json
import importlib
import get_ner
importlib.reload(get_ner)

# read in project src
with open('project_config.json','r') as fp: 
    news_tiers = json.load(fp)

from get_ner import *
import get_ner

# connect to client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY_GPT4"),
    api_version="2023-12-01-preview",
    azure_endpoint= "https://rfaz-openai-gpt4.openai.azure.com"
)

##### Prompt guidelines ######

query = """
"Without a lot of fanfare, drug counselor Miles Hamlin opened a resource hub in north Minneapolis on Tuesday for drug users to get sterile needles, fentanyl test strips and Narcan. They can shower, do their laundry and cook a meal. People who come might even use drugs on site. The staff will be trained to reverse overdoses.
"We're really trying to just focus on being a resource for people who use drugs to access no-barriers services," Hamlin said, emphasizing that he would allow clients and the surrounding community to dictate how the center is used.
Hamlin founded the nonprofit Minnesota Overdose Awareness in 2022 after more than a decade holding vigils in Loring Park for friends and clients who have died, trying to bring attention to Minneapolis' large racial disparities in overdoses. There were more than 1,000 fatal opioid overdoses in 2022 statewide, according to the Minnesota Department of Health. In the city of Minneapolis, Black people are four times more likely to die of an opioids than whites. For Native Americans, it's 30 to 1.
To shift the public health response to one that embraces harm reduction a medical philosophy that focuses on keeping drug users alive and reducing the spread of disease so they can eventually recover last year the Legislature legalized and funded "safe recovery" start-ups that by definition include safe injection spaces, needle exchange and other health services.
Minnesota Overdose Awareness' "Northside Hub" at 3859 Fremont Ave. N. technically includes every feature listed in the statute, but the nonprofit is keenly aware of the sensitivity surrounding ideas of "safe injection" or "overdose prevention" sites. Federal law still prohibits managing any facility "for the purpose of using a controlled substance," and local communities don't have much experience with them.
Last month, the Minneapolis City Council's public health committee approved a joint grant application with Saint Paul to research and conduct community engagement around safe recovery sites, but the vote wasn't unanimous, with. Council Member Michael Rainville opposed. He did not say why.
Before launching, Minnesota Overdose Awareness sought the approval of the Webber-Camden Neighborhood Association.
There was a lot of discussion. And while some community members attended the meeting to express their concerns and objections about how many people were going to congregate at the center and if there would be problems in the area after they left, the board felt their questions were answered "positively," said Patricia Deinhart-Bauknight, the association's executive director. "And you know, it's a need in the community for sure."
It's no secret that public drug use exists in the neighborhood, and it would be helpful to have more candid resources, including naloxone training, she said.
"I just got a call [Tuesday] morning from a community member about drug dealing all around his house and he can't get response from 311," Deinhart-Bauknight said. "One of our past board members is having an issue because he owns a mini grocery store in the community and people are hanging out in the back and stuff."
On Monday, Minnesota Overdose Awareness held an open house attended by dozens of harm reduction healthcare workers from across the metro. They showed off the renovated interior of what had been a dilapidated and water-damaged building that housed a former illegal nightclub run by the Zodiac Biker Club a decade ago. Board member John Roder fixed it up for about half a million dollars. There's an office full of clean injection supplies, roomy bathrooms, washing machines, a kitchen and a den with a computer to browse job openings.
Other rooms are kept open for future partnerships. Board chair Paula DeSanto said the nonprofit is talking with Helix, a rapid homeless rehousing company, and the nearby Fremont Clinic, a primary care family practice.
"We have to try all kinds of things," said Helix co-founder Adam Fairbanks. "So if the general population of Minneapolis is sick of having people on the streets, or super intoxicated at a bus stop ... if we all decide that this is a good place for people to go, then I think there's the support that's needed to change the local laws to allow it."
Jack Martin of Southside Harm Reduction Services, a group that delivers safe-use supplies, also attended the open house and came away with hope. In 2022, Southside Harm Reduction, as a sponsored organization of the Native American Community Clinic, received more than $5 million from the Bush Foundation to lay the groundwork for a south Minneapolis drop-in center that would provide a range of harm reduction services for people who use drugs, focusing on those who are also homeless and living unsheltered. That center is also envisioned as one that would be designed to pivot into a safe recovery center "if and when the community and city are ready."
No Southside site has yet been identified, but the group is aiming to open in 2025.
"It's beautiful," Martin said of the Northside Hub. "And the services are absolutely needed over north, in terms of harm reduction, supplies, training and services staff. We're really excited for them to open and can't wait to see what happens.""
"""
