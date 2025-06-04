import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK data
nltk.download('stopwords')
nltk.download('punkt')

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Join tokens back into text
    return ' '.join(tokens)

def train_sentiment_model():
    # Sample training data (in a real application, this would come from your database)
    data = {
        'text': [
            "This book is amazing! I couldn't put it down.",
            "The worst book I've ever read. Terrible plot and characters.",
            "It was okay, not great but not bad either.",
            "I loved every page of this book. Highly recommended!",
            "The writing style was poor and the story was boring.",
            "An average book with some good moments.",
            "This is a masterpiece of literature.",
            "I regret buying this book. Waste of time.",
            "The book was interesting but could be better.",
            "One of the best books I've read this year!"
        ],
        'sentiment': [
            'positive',
            'negative',
            'neutral',
            'positive',
            'negative',
            'neutral',
            'positive',
            'negative',
            'neutral',
            'positive'
        ]
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Preprocess text
    df['processed_text'] = df['text'].apply(preprocess_text)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        df['processed_text'],
        df['sentiment'],
        test_size=0.2,
        random_state=42
    )
    
    # Vectorize text
    vectorizer = TfidfVectorizer(max_features=1000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Train model
    model = LogisticRegression(multi_class='multinomial', solver='lbfgs')
    model.fit(X_train_vec, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test_vec)
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model and vectorizer
    os.makedirs('models', exist_ok=True)
    with open('models/sentiment_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    with open('models/vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    
    print("Model and vectorizer saved successfully!")

if __name__ == '__main__':
    train_sentiment_model() 