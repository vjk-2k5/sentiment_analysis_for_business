import spacy
import pandas as pd
from finbert_analysis import analyze_sentiment, get_recommendation
from emoji_sentiment import load_emoji_data, analyze_emoji_sentiment
from general_statement_analysis import analyze_general_statements  


nlp = spacy.load('en_core_web_sm')


def load_financial_terms(csv_file):
    df = pd.read_csv(csv_file, header=0)
    financial_terms = df['term'].tolist()
    return financial_terms


financial_terms = load_financial_terms('C:\\Rohit\\Projects\Fintech\\sentiment_analysis_for_business\\emoji_analysis\\financial_terms.csv')


def load_emoji_data(csv_file):
    emoji_df = pd.read_csv(csv_file, header=0)
    return emoji_df['Emoji'].tolist(), emoji_df


def segment_sentences(paragraph):
    doc = nlp(paragraph)
    return [sent.text for sent in doc.sents]


def classify_sentence(sentence, financial_terms):
    if any(term.lower() in sentence.lower() for term in financial_terms):
        return "financial"
    else:
        return "general"


def extract_emojis(paragraph, emoji_list):
    return [char for char in paragraph if char in emoji_list]


def classify_paragraph(paragraph, emoji_list, emoji_sentiment_data):
    sentences = segment_sentences(paragraph)
    classified_sentences = []

    
    for sentence in sentences:
        classification = classify_sentence(sentence, financial_terms)
        classified_sentences.append((sentence, classification))
    
    
    extracted_emojis = extract_emojis(paragraph, emoji_list)

    
    financial_statements = [sentence for sentence, classification in classified_sentences if classification == "financial"]
    sentiment_results = [(statement, analyze_sentiment(statement)) for statement in financial_statements]
    
    
    recommendations = {statement: get_recommendation(sentiment) for statement, sentiment in sentiment_results}

    
    emoji_sentiment = analyze_emoji_sentiment(extracted_emojis, emoji_sentiment_data)

    
    general_statements = [sentence for sentence, classification in classified_sentences if classification == "general"]
    analyzed_general_statements = [(statement, analyze_general_statements(statement)) for statement in general_statements]

    return classified_sentences, len(extracted_emojis), recommendations, emoji_sentiment, analyzed_general_statements


if __name__ == "__main__":
    paragraph = """
     The stock market is declining! 😭 I made a huge loss on my investment😔. 
    The weather is harsh today, and I feel lazy. 🌞
    """

    
    emoji_list, emoji_sentiment_data = load_emoji_data('C:\\Rohit\\Projects\Fintech\\sentiment_analysis_for_business\\emoji_analysis\\Emoji_Sentiment_Data_v1.0.csv')

    
    classified_results, emoji_count, recommendations, emoji_sentiment, analyzed_general_statements = classify_paragraph(paragraph, emoji_list, emoji_sentiment_data)

    
    for sentence, classification in classified_results:
        print(f"Sentence: {sentence.strip()}\nType: {classification}\n")

    
    print(f"Total Emojis: {emoji_count}\n")

    
    for statement, recommendation in recommendations.items():
        print(f"Financial Statement: {statement.strip()}\nRecommendation: {recommendation}\n")

    
    print("\nGeneral Statements and Recommendations:\n")
    for analysis in analyzed_general_statements:
        statement = analysis[0]  
        
        general_analysis = analysis[1][0]  

        sentiment = general_analysis['sentiment'] 
        recommendation = general_analysis['recommendation'] 

        print(f"General Statement: {statement}")
        print(f"Sentiment: {sentiment}")
        print(f"Recommendation: {recommendation}\n")




