import joblib


BNBmodel = joblib.load('bernoulli_nb_model.pkl')
vectoriser = joblib.load('vectoriser.pkl')

def predict_sentiment(sentence):

    sentence_vectorized = vectoriser.transform([sentence])
    prediction = BNBmodel.predict(sentence_vectorized)
    return prediction[0]  


def get_recommendation(sentiment):
    if sentiment == "very positive" or sentiment == "positive":
        return "Keep up the good work!"
    elif sentiment == "very negative" or sentiment == "negative":
        return "Consider reviewing your strategies."
    else:
        return "Stay informed about current trends."
    
def analyze(sentence):
    sentiment = predict_sentiment(sentence)
    general_statements = []
    if sentiment == 0:
        sentiment = "Negative"
    else :
        sentiment = "Positive"
    recommendation = get_recommendation(sentiment)
    
    general_statements.append({
            'statement': sentence,
            'sentiment': sentiment,
            'recommendation': recommendation
        })

    return general_statements  


