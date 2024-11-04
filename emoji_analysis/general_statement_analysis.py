import spacy
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.preprocessing import LabelEncoder
import numpy as np


nlp = spacy.load('en_core_web_sm')


model_name = 'nlptown/bert-base-multilingual-uncased-sentiment'  
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)


label_encoder = LabelEncoder()
label_encoder.classes_ = np.array(['very negative', 'negative', 'neutral', 'positive', 'very positive'])  # Adjust classes based on your model


def segment_sentences(paragraph):
    doc = nlp(paragraph)
    return [sent.text for sent in doc.sents]


def analyze_sentiment(statement):
    inputs = tokenizer(statement, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    sentiment_label = label_encoder.inverse_transform([torch.argmax(logits).item()])
    return sentiment_label[0]


def get_recommendation(sentiment):
    if sentiment == "very positive" or sentiment == "positive":
        return "Keep up the good work!"
    elif sentiment == "very negative" or sentiment == "negative":
        return "Consider reviewing your strategies."
    else:
        return "Stay informed about current trends."


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

    return general_statements  

