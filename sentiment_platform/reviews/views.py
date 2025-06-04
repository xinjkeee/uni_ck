from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.db.models import Count, Avg
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
from django.core.exceptions import PermissionDenied

from .models import Book, Review, UserProfile, SentimentAnalysis, BookCategory, ReviewRating
from .forms import (
    UserRegisterForm, UserProfileForm, BookForm, ReviewForm,
    ReviewRatingForm, BookCategoryForm, CSVUploadForm, ReviewFilterForm, BookFilterForm
)

def get_sentiment_from_rating(rating):
    """Convert numerical rating to sentiment category"""
    if rating >= 4:
        return 'positive'
    elif rating <= 2:
        return 'negative'
    return 'neutral'

def home(request):
    # Get statistics for the dashboard
    total_books = Book.objects.count()
    total_reviews = Review.objects.count()
    sentiment_counts = Review.objects.values('sentiment').annotate(count=Count('sentiment'))
    
    # Get recent books and reviews
    recent_books = Book.objects.order_by('-created_at')[:5]
    recent_reviews = Review.objects.order_by('-created_at')[:5]
    
    # Create pie chart
    plt.figure(figsize=(8, 6))
    sentiments = [item['sentiment'] for item in sentiment_counts]
    counts = [item['count'] for item in sentiment_counts]
    plt.pie(counts, labels=sentiments, autopct='%1.1f%%')
    plt.title('Review Sentiment Distribution')
    
    # Convert plot to base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plot_data = base64.b64encode(image_png).decode('utf-8')
    
    context = {
        'total_books': total_books,
        'total_reviews': total_reviews,
        'plot_data': plot_data,
        'recent_books': recent_books,
        'recent_reviews': recent_reviews
    }
    
    return render(request, 'reviews/home.html', context)

class BookListView(ListView):
    model = Book
    template_name = 'reviews/book_list.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BookFilterForm(self.request.GET)
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'reviews/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(book=self.object)
        return context

class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'reviews/book_form.html'
    success_url = reverse_lazy('book-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'reviews/book_form.html'
    success_url = reverse_lazy('book-list')

class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'reviews/book_confirm_delete.html'
    success_url = reverse_lazy('book-list')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'reviews/register.html', {'form': form})

@login_required
def profile(request):
    # Get or create the user profile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    user_reviews = Review.objects.filter(user=request.user)
    return render(request, 'reviews/profile.html', {
        'form': form,
        'user_reviews': user_reviews
    })

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.kwargs.get('pk')
        context['book'] = get_object_or_404(Book, pk=book_id)
        return context

    def form_valid(self, form):
        book_id = self.kwargs.get('pk')
        book = get_object_or_404(Book, pk=book_id)
        form.instance.user = self.request.user
        form.instance.book = book
        return super().form_valid(form)

    def get_success_url(self):
        book_id = self.kwargs.get('pk')
        return reverse('book-detail', kwargs={'pk': book_id})

@login_required
def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            has_header = form.cleaned_data['has_header']
            
            try:
                df = pd.read_csv(csv_file)
                for _, row in df.iterrows():
                    book = Book.objects.create(
                        title=row['title'],
                        author=row['author'],
                        description=row['description'],
                        published_date=row['published_date']
                    )
                messages.success(request, 'CSV file uploaded successfully!')
            except Exception as e:
                messages.error(request, f'Error uploading CSV file: {str(e)}')
            
            return redirect('book-list')
    else:
        form = CSVUploadForm()
    return render(request, 'reviews/upload_csv.html', {'form': form})

def review_list(request):
    form = ReviewFilterForm(request.GET)
    reviews = Review.objects.all()
    
    if form.is_valid():
        sentiment = form.cleaned_data.get('sentiment')
        book = form.cleaned_data.get('book')
        
        if sentiment:
            reviews = reviews.filter(sentiment=sentiment)
        if book:
            reviews = reviews.filter(book=book)
    
    context = {
        'reviews': reviews,
        'form': form
    }
    
    return render(request, 'reviews/review_list.html', context)

class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_confirm_delete.html'
    
    def get_success_url(self):
        return reverse('book-detail', kwargs={'pk': self.object.book.pk})

    def get_object(self, queryset=None):
        review = super().get_object(queryset)
        if not review.can_delete(self.request.user):
            raise PermissionDenied("You don't have permission to delete this review")
        return review
