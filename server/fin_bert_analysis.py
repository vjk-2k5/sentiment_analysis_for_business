import torch
from transformers import BertTokenizer, BertForSequenceClassification


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=3)
model.load_state_dict(torch.load('C:\\Rohit\\Projects\\Fintech\\sentiment_analysis_for_business\\fin_bert_trained_with_colab\\finetuned_finBERT_epoch_1.model', map_location=device))
model.to(device)
model.eval()


tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')


def preprocess_text(text, max_length=128):
    encoding = tokenizer(
        text,
        truncation=True,
        padding='max_length',
        max_length=max_length,
        return_tensors='pt'
    )
    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)
    return input_ids, attention_mask


def predict_sentiment(text):
    input_ids, attention_mask = preprocess_text(text)


    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits


    probabilities = torch.softmax(logits, dim=1)
    predicted_class = torch.argmax(probabilities, dim=1).item()

    return predicted_class, probabilities[0].cpu().numpy()

def get_recommendation(sentiment):
    if sentiment == "Positive":
        return "Share this positive news with your followers to boost confidence and engagement!"
    elif sentiment == "Negative":
        return "Consider addressing concerns transparently to maintain trust among your stakeholders."
    else:
        return "Try to improve your current strategy while monitoring the situation; clarity is key."

#text = " The stock market is declining! 😭 I made a huge loss on my investment😔.The weather is harsh today, and I feel lazy. 🌞"

def finbertAnalysis(text):
    predicted_class, probabilities = predict_sentiment(text)
    

    if predicted_class == 0:
        sentiment = "Neutral"
    elif predicted_class == 1:
        sentiment = "Negative"
    else:
        sentiment = "Positive"
    recommendation = get_recommendation(sentiment)
    return  sentiment, recommendation, probabilities




#print(f"Predicted class: {predicted_class}")
#print(f"Sentiment : {sentiment}")
#print(f"Probabilities: {probabilities}")
