import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model # type: ignore
from sklearn.preprocessing import StandardScaler

# Load the trained model
model = load_model('Sentiment Analysis for business\emoji_sentiment_model.h5')

# Load emoji sentiment data from CSV
def load_emoji_data(csv_file):
    df = pd.read_csv(csv_file)
    return df['Emoji'].tolist(), df

# Function to preprocess the emoji sentiment data
def preprocess_data(emoji_sentiment_df):
    # Extract the features from the dataframe
    X = emoji_sentiment_df[['Negative', 'Neutral', 'Positive']].values
    # Scale the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled

# Function to predict sentiment based on emojis
def analyze_emoji_sentiment(extracted_emojis, emoji_sentiment_data):
    positive_count = 0
    negative_count = 0
    neutral_count = 0

    # Analyze each emoji in the extracted emojis
    for emoji in extracted_emojis:
        # Check if the emoji exists in the sentiment data
        if emoji in emoji_sentiment_data['Emoji'].values:
            sentiment_data = emoji_sentiment_data[emoji_sentiment_data['Emoji'] == emoji].iloc[0]
            negative = sentiment_data['Negative']
            neutral = sentiment_data['Neutral']
            positive = sentiment_data['Positive']

            # Count the highest sentiment type
            if positive > negative and positive > neutral:
                positive_count += 1
            elif negative > positive and negative > neutral:
                negative_count += 1
            else:
                neutral_count += 1

    # Determine overall sentiment
    if positive_count > negative_count:
        return "Positive"
    elif negative_count > positive_count:
        return "Negative"
    else:
        return "Neutral"


