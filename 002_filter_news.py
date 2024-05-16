import json
import pandas
import pickle

# read in news tiers
with open('src/news_tiers.json','r') as fp: 
    news_tiers = json.load(fp)


# read in data
df = pd.read_csv("opioids_reduce_prevention_2024-01-01_2024-05-16_.csv")
print("Shape for original dataframe:", df.shape)

# map news sources to tiers
given_sources = df["source_name"].unique()

# Map each source to its appropriate tier
source_map = {}
for tier, sources in news_tiers.items():
    for source in sources:
        source_map[source] = tier

# Now map the given sources
mapped_sources = {}
for source in given_sources:
    # Check and place in the right category or default to a suitable category if not found
    mapped_sources[source] = source_map.get(source, "General Interest & Mixed Quality")

# Add rank to dataframe
news_ranked = pd.DataFrame(list(mapped_sources.items()), columns=['source_name', 'rank'])
# combine with original df
df_ranked = pd.merge(df, news_ranked,how = "left", on = "source_name")


# select types of news that we want
quality_list = ["Top Tier News Sources", "Market Trends & Mixed Quality", "Local News Sources", "High-Quality News Sources", "Medical & Mixed Quality", "Scientific & High Quality", "Reliable Specialized Sources", "Legal & Mixed Quality"]

# filter dataframe for only quality sources
dfq = df_ranked[df_ranked["rank"].isin(quality_list)]
print("Shape for filtered dataframe by news tiers:", dfq.shape)

# write to 
output = open("news_filtered.pkl" , "wb")
pickle.dump(dfq, output)