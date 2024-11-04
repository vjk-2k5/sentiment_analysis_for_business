import spacy
import pandas as pd
from finbert_analysis import analyze_sentiment, get_recommendation
from emoji_sentiment import load_emoji_data, analyze_emoji_sentiment
from general_statement_analysis import analyze_general_statements  # Importing the new module

# Load the spaCy NLP model for sentence segmentation
nlp = spacy.load('en_core_web_sm')

# Function to load financial terms from a CSV file
def load_financial_terms(csv_file):
    df = pd.read_csv(csv_file, header=0)
    financial_terms = df['term'].tolist()
    return financial_terms

# Load the financial terms from the CSV file
financial_terms = load_financial_terms('Sentiment Analysis for business//financial_terms.csv')

# Function to load the emoji sentiment data from the CSV
def load_emoji_data(csv_file):
    emoji_df = pd.read_csv(csv_file, header=0)
    return emoji_df['Emoji'].tolist(), emoji_df

# Segment paragraph into sentences using spaCy
def segment_sentences(paragraph):
    doc = nlp(paragraph)
    return [sent.text for sent in doc.sents]

# Function to classify each sentence as financial or general
def classify_sentence(sentence, financial_terms):
    if any(term.lower() in sentence.lower() for term in financial_terms):
        return "financial"
    else:
        return "general"

# Function to extract emojis from the paragraph by matching against the emoji list
def extract_emojis(paragraph, emoji_list):
    return [char for char in paragraph if char in emoji_list]

# Main function to classify sentences, count emojis, and perform sentiment analysis
def classify_paragraph(paragraph, emoji_list, emoji_sentiment_data):
    sentences = segment_sentences(paragraph)
    classified_sentences = []

    # Classify each sentence as financial or general
    for sentence in sentences:
        classification = classify_sentence(sentence, financial_terms)
        classified_sentences.append((sentence, classification))
    
    # Extract emojis from the paragraph using the emoji list
    extracted_emojis = extract_emojis(paragraph, emoji_list)

    # Analyze financial statements for sentiment using FinBERT
    financial_statements = [sentence for sentence, classification in classified_sentences if classification == "financial"]
    sentiment_results = [(statement, analyze_sentiment(statement)) for statement in financial_statements]
    
    # Prepare recommendations based on sentiment for financial statements
    recommendations = {statement: get_recommendation(sentiment) for statement, sentiment in sentiment_results}

    # Analyze emoji sentiment using the extracted emojis and the sentiment data
    emoji_sentiment = analyze_emoji_sentiment(extracted_emojis, emoji_sentiment_data)

    # Analyze only general statements using the separate module
    general_statements = [sentence for sentence, classification in classified_sentences if classification == "general"]
    analyzed_general_statements = [(statement, analyze_general_statements(statement)) for statement in general_statements]

    return classified_sentences, len(extracted_emojis), recommendations, emoji_sentiment, analyzed_general_statements

# Example usage
if __name__ == "__main__":
    paragraph = """
     The stock market is declining! 😭 I made a huge loss on my investment😔. 
    The weather is harsh today, and I feel lazy. 🌞
    """

    # Load emoji sentiment data from the CSV file
    emoji_list, emoji_sentiment_data = load_emoji_data('Sentiment Analysis for business\\Emoji_Sentiment_Data_v1.0.csv')

    # Classify the paragraph and perform sentiment analysis
    classified_results, emoji_count, recommendations, emoji_sentiment, analyzed_general_statements = classify_paragraph(paragraph, emoji_list, emoji_sentiment_data)

    # Print classified sentences
    for sentence, classification in classified_results:
        print(f"Sentence: {sentence.strip()}\nType: {classification}\n")

    # Print the total number of emojis in the paragraph
    print(f"Total Emojis: {emoji_count}\n")

    # Print recommendations based on financial sentiment
    for statement, recommendation in recommendations.items():
        print(f"Financial Statement: {statement.strip()}\nRecommendation: {recommendation}\n")

    # Print general statements with sentiment and recommendations
    print("\nGeneral Statements and Recommendations:\n")
    for analysis in analyzed_general_statements:
        statement = analysis[0]  # The general statement
        # Extract the dictionary from the second element, assuming it has only one dictionary
        general_analysis = analysis[1][0]  # Get the first (and only) dictionary

        sentiment = general_analysis['sentiment']  # Extract the sentiment
        recommendation = general_analysis['recommendation']  # Extract the recommendation

        print(f"General Statement: {statement}")
        print(f"Sentiment: {sentiment}")
        print(f"Recommendation: {recommendation}\n")




