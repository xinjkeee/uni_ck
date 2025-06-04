from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Review, UserProfile, BookCategory, ReviewRating

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']

class BookForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=BookCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'published_date', 'cover_image', 'categories']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        }
        labels = {
            'text': 'Your Review'
        }

class ReviewRatingForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['rating']

class BookCategoryForm(forms.ModelForm):
    class Meta:
        model = BookCategory
        fields = ['name', 'description']

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Select a CSV file')
    has_header = forms.BooleanField(label='CSV has header row', required=False, initial=True)

class ReviewFilterForm(forms.Form):
    SENTIMENT_CHOICES = [
        ('', 'All'),
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
    ]
    
    sentiment = forms.ChoiceField(
        choices=SENTIMENT_CHOICES,
        required=False,
        label='Filter by Sentiment'
    )
    
    book = forms.ModelChoiceField(
        queryset=Book.objects.all(),
        required=False,
        label='Filter by Book'
    )

class BookFilterForm(forms.Form):
    title = forms.CharField(required=False)
    author = forms.CharField(required=False)
    category = forms.ModelChoiceField(
        queryset=BookCategory.objects.all(),
        required=False,
        empty_label="All Categories"
    ) 