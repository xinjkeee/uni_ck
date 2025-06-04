from django.contrib import admin
from .models import (
    Book, Review, UserProfile, SentimentAnalysis,
    BookCategory, BookCategoryMapping, ReviewRating
)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'created_at')
    search_fields = ('title', 'author')
    list_filter = ('published_date', 'created_at')
    date_hierarchy = 'published_date'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'sentiment', 'created_at')
    search_fields = ('text', 'book__title', 'user__username')
    list_filter = ('sentiment', 'created_at')
    date_hierarchy = 'created_at'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_guest')
    search_fields = ('user__username', 'bio')
    list_filter = ('is_guest',)

@admin.register(SentimentAnalysis)
class SentimentAnalysisAdmin(admin.ModelAdmin):
    list_display = ('review', 'positive_score', 'negative_score', 'neutral_score', 'analyzed_at')
    search_fields = ('review__text',)
    list_filter = ('analyzed_at',)

@admin.register(BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')

@admin.register(BookCategoryMapping)
class BookCategoryMappingAdmin(admin.ModelAdmin):
    list_display = ('book', 'category')
    search_fields = ('book__title', 'category__name')
    list_filter = ('category',)

@admin.register(ReviewRating)
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('review', 'rating', 'created_at')
    search_fields = ('review__text',)
    list_filter = ('rating', 'created_at')
    date_hierarchy = 'created_at'
