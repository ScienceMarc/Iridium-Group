from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from .models import Book, Borrower, BookLoan, Fine
from datetime import datetime, timedelta

def home(request):
    return render(request, 'libraryapp/home.html')

def search_books(request):
    query = request.GET.get('q', '')
    books = []
    
    if query:
        # Search across ISBN, title, and authors
        books = Book.objects.filter(
            Q(isbn__icontains=query) |
            Q(title__icontains=query) |
            Q(authors__name__icontains=query)
        ).distinct()
        
        # Annotate with loan status
        for book in books:
            active_loan = BookLoan.objects.filter(book=book, date_in__isnull=True).first()
            book.is_checked_out = active_loan is not None
            book.borrower_id = active_loan.borrower.card_no if active_loan else None
    
    return render(request, 'libraryapp/search_books.html', {
        'books': books,
        'query': query
    })

def checkout_book(request):
    if request.method == 'POST':
        isbn = request.POST.get('isbn')
        card_no = request.POST.get('card_no')
        
        try:
            book = Book.objects.get(isbn=isbn)
            borrower = Borrower.objects.get(card_no=card_no)
            
            # Check if book is already checked out
            if BookLoan.objects.filter(book=book, date_in__isnull=True).exists():
                messages.error(request, 'This book is already checked out.')
                return redirect('search_books')
            
            # Check if borrower has 3 active loans
            active_loans = BookLoan.objects.filter(borrower=borrower, date_in__isnull=True).count()
            if active_loans >= 3:
                messages.error(request, 'Borrower has reached the maximum limit of 3 active loans.')
                return redirect('search_books')
            
            # Check if borrower has unpaid fines
            unpaid_fines = Fine.objects.filter(loan__borrower=borrower, paid=False).exists()
            if unpaid_fines:
                messages.error(request, 'Borrower has unpaid fines and cannot check out books.')
                return redirect('search_books')
            
            # Create new loan
            BookLoan.objects.create(
                book=book,
                borrower=borrower,
                date_out=datetime.now().date(),
                due_date=datetime.now().date() + timedelta(days=14)
            )
            messages.success(request, 'Book checked out successfully!')
            
        except Book.DoesNotExist:
            messages.error(request, 'Book not found.')
        except Borrower.DoesNotExist:
            messages.error(request, 'Borrower not found.')
            
    return redirect('search_books')

def checkin_book(request):
    if request.method == 'POST':
        loan_id = request.POST.get('loan_id')
        try:
            loan = BookLoan.objects.get(loan_id=loan_id)
            loan.date_in = datetime.now().date()
            loan.save()
            messages.success(request, 'Book checked in successfully!')
        except BookLoan.DoesNotExist:
            messages.error(request, 'Loan not found.')
    return redirect('search_books')

def manage_fines(request):
    query = request.GET.get('q', '')
    fines = []
    
    if query:
        fines = Fine.objects.filter(
            Q(loan__borrower__card_no__icontains=query) |
            Q(loan__borrower__fname__icontains=query) |
            Q(loan__borrower__lname__icontains=query)
        ).select_related('loan__borrower')
    
    return render(request, 'libraryapp/manage_fines.html', {
        'fines': fines,
        'query': query
    })

def pay_fine(request):
    if request.method == 'POST':
        fine_id = request.POST.get('fine_id')
        try:
            fine = Fine.objects.get(id=fine_id)
            if fine.loan.date_in is None:
                messages.error(request, 'Cannot pay fine for a book that is still checked out.')
            else:
                fine.paid = True
                fine.save()
                messages.success(request, 'Fine paid successfully!')
        except Fine.DoesNotExist:
            messages.error(request, 'Fine not found.')
    return redirect('manage_fines')
