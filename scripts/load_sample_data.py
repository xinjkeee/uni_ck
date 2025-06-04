import json
import os
import django
import sys
from datetime import datetime
from django.utils import timezone

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sentiment_platform.settings')
django.setup()

from reviews.models import Book, Review, User
from django.contrib.auth.hashers import make_password

def load_sample_data():
    # Read the sample data file
    with open('scripts/sample_reviews.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Process each book
    for book_data in data['books']:
        # Create or get the book
        book, created = Book.objects.get_or_create(
            title=book_data['title'],
            defaults={
                'author': book_data['author'],
                'description': book_data['description'],
                'published_date': timezone.now().date()
            }
        )
        
        print(f"Processing book: {book.title}")
        
        # Process each review
        for review_data in book_data['reviews']:
            # Create or get the user
            user, created = User.objects.get_or_create(
                username=review_data['author'],
                defaults={
                    'password': make_password('dummy_password'),
                    'email': f"{review_data['author'].lower()}@example.com"
                }
            )
            
            # Convert rating to sentiment
            rating = review_data['rating']
            if rating >= 4:
                sentiment = 'positive'
            elif rating <= 2:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            # Create the review
            review, created = Review.objects.get_or_create(
                book=book,
                user=user,
                defaults={
                    'text': review_data['text'],
                    'sentiment': sentiment,
                    'created_at': datetime.strptime(review_data['date'], '%Y-%m-%d').date()
                }
            )
            
            if created:
                print(f"Created review by {user.username} for {book.title}")
            else:
                print(f"Review by {user.username} for {book.title} already exists")

if __name__ == "__main__":
    load_sample_data()
    print("Sample data loading completed!") 