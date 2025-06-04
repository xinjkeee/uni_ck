from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/new/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('books/<int:pk>/review/', views.ReviewCreateView.as_view(), name='review-create'),
    path('reviews/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review-delete'),
    path('reviews/', views.review_list, name='review-list'),
    path('upload-csv/', views.upload_csv, name='upload-csv'),
] 