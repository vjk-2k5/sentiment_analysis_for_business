from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load the FinBERT model and tokenizer
model_name = "ProsusAI/finBERT"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

def analyze_sentiment(statement):
    inputs = tokenizer(statement, return_tensors="pt", padding=True, truncation=True, max_length=512)
    
    # Get model predictions
    with torch.no_grad():
        outputs = model(**inputs)
        
    # Get predicted class
    predicted_class = torch.argmax(outputs.logits, dim=1).item()
    
    # Map predicted class to sentiment
    sentiment_map = {
        0: "Negative",
        1: "Neutral",
        2: "Positive"
    }
    
    sentiment = sentiment_map.get(predicted_class, "Unknown")
    return sentiment

def get_recommendation(sentiment):
    if sentiment == "Positive":
        return "Share this positive news with your followers to boost confidence and engagement!"
    elif sentiment == "Negative":
        return "Consider addressing concerns transparently to maintain trust among your stakeholders."
    else:
        return "Try to improve your current strategy while monitoring the situation; clarity is key."
