from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book-search/', views.book_search, name='book_search'),
    path('book-loans/', views.book_loans, name='book_loans'),
    path('borrower-management/', views.borrower_management, name='borrower_management'),
    path('fines/', views.fines, name='fines'),
] 