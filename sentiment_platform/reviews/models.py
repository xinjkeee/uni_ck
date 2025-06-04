from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .sentiment_analyzer import SentimentAnalyzer

class UserRole(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Administrator'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='role')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

    def is_admin(self):
        return self.role == 'admin'

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    published_date = models.DateField(null=True, blank=True)
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

class Review(models.Model):
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES, blank=True)
    sentiment_score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.sentiment:  # Only analyze if sentiment is not already set
            analyzer = SentimentAnalyzer()
            self.sentiment, self.sentiment_score = analyzer.analyze(self.text)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review of {self.book.title} by {self.user.username}"

    def can_delete(self, user):
        """Check if the given user can delete this review"""
        if not user.is_authenticated:
            return False
        if user.role.is_admin():
            return True
        return self.user == user

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    is_guest = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s profile"

class SentimentAnalysis(models.Model):
    review = models.OneToOneField(Review, on_delete=models.CASCADE)
    positive_score = models.FloatField()
    negative_score = models.FloatField()
    neutral_score = models.FloatField()
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sentiment analysis for review {self.review.id}"

class BookCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class BookCategoryMapping(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book.title} - {self.category.name}"

class ReviewRating(models.Model):
    review = models.OneToOneField(Review, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating {self.rating} for review {self.review.id}"
