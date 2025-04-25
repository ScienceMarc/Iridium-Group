from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_books, name='search_books'),
    path('checkout/', views.checkout_book, name='checkout_book'),
    path('checkin/', views.checkin_book, name='checkin_book'),
    path('fines/', views.manage_fines, name='manage_fines'),
    path('pay-fine/', views.pay_fine, name='pay_fine'),
] 