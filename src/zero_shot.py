from transformers import pipeline
classifier = pipeline("zero-shot-classification", model="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli")

# load in pandas and numpy for data manipulation
import pandas as pd
import numpy as np

def predict_sentiment(df, text_column, text_labels):
    """
    Predict the sentiment for a piece of text in a dataframe.

    Args:
        df (pandas.DataFrame): A DataFrame containing the text data to perform sentiment analysis on.
        text_column (str): The name of the column in the DataFrame that contains the text data.
        text_labels (list): A list of text labels for sentiment classification.

    Returns:
        pandas.DataFrame: A DataFrame containing the original data with additional columns for the predicted 
        sentiment label and corresponding score.

    Raises:
        ValueError: If the DataFrame (df) does not contain the specified text_column.

    Example:
        # Assuming df is a pandas DataFrame and text_labels is a list of text labels
        result = predict_sentiment(df, "text_column_name", text_labels)
    """
    
    result_list = []
    for index, row in df.iterrows():
        sequence_to_classify = row[text_column]
        result = classifier(sequence_to_classify, text_labels, multi_label = False)
        result['sentiment'] = result['labels'][0]
        result['score'] = result['scores'][0]
        result_list.append(result)
    result_df = pd.DataFrame(result_list)[['sequence', 'sentiment', 'score']]
    result_df = pd.merge(df, result_df, left_on = text_column, right_on="sequence", how = "left")
    return result_df

