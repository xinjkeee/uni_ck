import os
import django
from django.contrib.auth.models import User
from reviews.models import Book, Review, UserProfile, BookCategory, BookCategoryMapping

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sentiment_platform.settings')
django.setup()

def create_sample_data():
    # Create categories
    fiction = BookCategory.objects.create(name='Fiction', description='Fictional books')
    non_fiction = BookCategory.objects.create(name='Non-Fiction', description='Non-fictional books')
    mystery = BookCategory.objects.create(name='Mystery', description='Mystery and thriller books')
    romance = BookCategory.objects.create(name='Romance', description='Romance novels')

    # Create sample books
    books = [
        {
            'title': 'The Great Gatsby',
            'author': 'F. Scott Fitzgerald',
            'description': 'A story of the fabulously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan.',
            'categories': [fiction]
        },
        {
            'title': 'To Kill a Mockingbird',
            'author': 'Harper Lee',
            'description': 'The story of racial injustice and the loss of innocence in the American South.',
            'categories': [fiction]
        },
        {
            'title': '1984',
            'author': 'George Orwell',
            'description': 'A dystopian social science fiction novel and cautionary tale.',
            'categories': [fiction]
        },
        {
            'title': 'The Da Vinci Code',
            'author': 'Dan Brown',
            'description': 'A mystery thriller novel that follows symbologist Robert Langdon.',
            'categories': [mystery]
        },
        {
            'title': 'Pride and Prejudice',
            'author': 'Jane Austen',
            'description': 'A romantic novel of manners.',
            'categories': [romance, fiction]
        }
    ]

    # Create books and category mappings
    for book_data in books:
        book = Book.objects.create(
            title=book_data['title'],
            author=book_data['author'],
            description=book_data['description']
        )
        for category in book_data['categories']:
            BookCategoryMapping.objects.create(book=book, category=category)

    # Create sample users
    users = [
        {'username': 'john_doe', 'email': 'john@example.com'},
        {'username': 'jane_smith', 'email': 'jane@example.com'},
        {'username': 'bob_wilson', 'email': 'bob@example.com'}
    ]

    for user_data in users:
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password='password123'
        )
        UserProfile.objects.create(user=user)

    print("Sample data created successfully!")

if __name__ == '__main__':
    create_sample_data() 