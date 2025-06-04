import json
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from datetime import datetime
from reviews.models import Book, Review, User
from django.utils import timezone

class Command(BaseCommand):
    help = 'Loads sample book reviews data into the database'

    def handle(self, *args, **options):
        # Get the absolute path to the sample data file
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        data_file = os.path.join(base_dir, 'sample_reviews.json')
        
        # Read the sample data file
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Process each book
        for book_data in data['reviews']:
            # Create or get the book
            book, created = Book.objects.get_or_create(
                title=book_data['book_title'],
                defaults={
                    'author': book_data['author'],
                    'description': 'Sample book description',  # Add a default description
                    'published_date': timezone.now().date()
                }
            )
            
            self.stdout.write(self.style.SUCCESS(f"Processing book: {book.title}"))
            
            # Process each review
            for review_data in book_data['reviews']:
                # Create or get the user
                user, created = User.objects.get_or_create(
                    username=review_data['reviewer'],
                    defaults={
                        'password': make_password('dummy_password'),
                        'email': f"{review_data['reviewer'].lower()}@example.com"
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
                    self.stdout.write(self.style.SUCCESS(f"Created review by {user.username} for {book.title}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Review by {user.username} for {book.title} already exists"))
        
        self.stdout.write(self.style.SUCCESS("Sample data loading completed!")) 