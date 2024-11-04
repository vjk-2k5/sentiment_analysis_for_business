import spacy
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Load the spaCy NLP model for sentence segmentation
nlp = spacy.load('en_core_web_sm')

# Load the pre-trained BERT model and tokenizer
model_name = 'nlptown/bert-base-multilingual-uncased-sentiment'  # You can change this to your preferred model
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Load label encoder for sentiment labels
label_encoder = LabelEncoder()
label_encoder.classes_ = np.array(['very negative', 'negative', 'neutral', 'positive', 'very positive'])  # Adjust classes based on your model

# Function to segment paragraph into sentences using spaCy
def segment_sentences(paragraph):
    doc = nlp(paragraph)
    return [sent.text for sent in doc.sents]

# Function to analyze sentiment using the BERT model
def analyze_sentiment(statement):
    inputs = tokenizer(statement, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    sentiment_label = label_encoder.inverse_transform([torch.argmax(logits).item()])
    return sentiment_label[0]

# Function to provide recommendations based on sentiment
def get_recommendation(sentiment):
    if sentiment == "very positive" or sentiment == "positive":
        return "Keep up the good work!"
    elif sentiment == "very negative" or sentiment == "negative":
        return "Consider reviewing your strategies."
    else:
        return "Stay informed about current trends."

# Function to analyze general statements
# Function to analyze general statements
def analyze_general_statements(paragraph):
    sentences = segment_sentences(paragraph)
    general_statements = []

    for sentence in sentences:
        sentiment = analyze_sentiment(sentence)
        recommendation = get_recommendation(sentiment)
        general_statements.append({
            'statement': sentence,
            'sentiment': sentiment,
            'recommendation': recommendation
        })

    return general_statements  # Ensure this returns a list of dictionaries

