from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q, Sum, Count, Case, When, BooleanField
from django.db.models.functions import Concat
from django.db.models import Value
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import Book, Author, Borrower, BookLoan, Fine
import re

def home(request):
    return render(request, 'libraryapp/home.html')

def book_search(request):
    query = request.GET.get('q', '')
    books = []
    
    if query:
        # Search in books and authors
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(isbn__icontains=query) |
            Q(authors__name__icontains=query)
        ).distinct()
        for book in books:
            active_loan = book.bookloan_set.filter(date_in__isnull=True).first()
            book.is_checked_out = bool(active_loan)
            book.borrower_id = active_loan.borrower.card_no if active_loan else None
    
    return render(request, 'libraryapp/book_search.html', {
        'books': books,
        'query': query
    })

def book_loans(request):
    search_query = request.GET.get('q', '').strip()
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'checkout':
            isbn = request.POST.get('isbn')
            card_no = request.POST.get('card_no')
            
            try:
                book = Book.objects.get(isbn=isbn)
                borrower = Borrower.objects.get(card_no=card_no)
                
                # Check if borrower has unpaid fines
                if Fine.objects.filter(loan__borrower=borrower, paid=False).exists():
                    messages.error(request, 'Borrower has unpaid fines and cannot check out books.')
                    return redirect('book_loans')
                
                # Check if borrower has reached limit
                active_loans = BookLoan.objects.filter(borrower=borrower, date_in__isnull=True).count()
                if active_loans >= 3:
                    messages.error(request, 'Borrower has reached the maximum number of active loans (3).')
                    return redirect('book_loans')
                
                # Check if book is available
                if BookLoan.objects.filter(book=book, date_in__isnull=True).exists():
                    messages.error(request, 'Book is already checked out.')
                    return redirect('book_loans')
                
                # Create new loan
                BookLoan.objects.create(
                    book=book,
                    borrower=borrower,
                    due_date=timezone.now().date() + timedelta(days=14)
                )
                messages.success(request, 'Book checked out successfully.')
                
            except (Book.DoesNotExist, Borrower.DoesNotExist):
                messages.error(request, 'Invalid ISBN or borrower card number.')
        
        elif action == 'checkin':
            isbn = request.POST.get('isbn')
            try:
                book = Book.objects.get(isbn=isbn)
                loan = BookLoan.objects.get(book=book, date_in__isnull=True)
                loan.date_in = timezone.now().date()
                loan.save()
                messages.success(request, 'Book checked in successfully.')
            except (Book.DoesNotExist, BookLoan.DoesNotExist):
                messages.error(request, 'No active loan found for this ISBN.')
    
    # Get active loans for display, with optional search
    active_loans = BookLoan.objects.filter(date_in__isnull=True)
    if search_query:
        active_loans = active_loans.filter(
            Q(book__isbn__icontains=search_query) |
            Q(borrower__card_no__icontains=search_query) |
            Q(borrower__fname__icontains=search_query) |
            Q(borrower__lname__icontains=search_query)
        )
    return render(request, 'libraryapp/book_loans.html', {
        'active_loans': active_loans,
        'search_query': search_query
    })

def borrower_management(request):
    if request.method == 'POST':
        ssn = request.POST.get('ssn')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        
        # Check if borrower with SSN already exists
        if Borrower.objects.filter(ssn=ssn).exists():
            messages.error(request, 'A borrower with this SSN already exists.')
            return redirect('borrower_management')
        
        # Generate new card number
        last_borrower = Borrower.objects.order_by('-card_no').first()
        if last_borrower:
            match = re.search(r'(\d+)$', last_borrower.card_no)
            if match:
                last_number = int(match.group(1))
                new_number = last_number + 1
                new_card_no = f"ID{new_number:06d}"
            else:
                new_card_no = "ID000001"
        else:
            new_card_no = "ID000001"
        
        # Create new borrower
        Borrower.objects.create(
            card_no=new_card_no,
            ssn=ssn,
            fname=fname,
            lname=lname,
            address=address,
            phone=phone
        )
        messages.success(request, f'New borrower created with card number: {new_card_no}')
    
    return render(request, 'libraryapp/borrower_management.html')

def fines(request):
    search_query = request.GET.get('q', '').strip()
    show_all = request.GET.get('show_all', '') == '1'
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_fines':
            # Update fines for all active loans
            for loan in BookLoan.objects.filter(date_in__isnull=True):
                if loan.due_date < timezone.now().date():
                    days_late = (timezone.now().date() - loan.due_date).days
                    fine_amount = Decimal(days_late) * Decimal('0.25')
                    
                    fine, created = Fine.objects.get_or_create(
                        loan=loan,
                        defaults={'fine_amt': fine_amount}
                    )
                    if not created and not fine.paid:
                        fine.fine_amt = fine_amount
                        fine.save()
        
        elif action == 'pay_fine':
            card_no = request.POST.get('fine_id')
            unpaid_fines = Fine.objects.filter(loan__borrower__card_no=card_no, paid=False)
            if unpaid_fines.filter(loan__date_in__isnull=True).exists():
                messages.error(request, 'Cannot pay fines: borrower has late books not yet returned.')
            elif unpaid_fines.exists():
                unpaid_fines.update(paid=True)
                messages.success(request, 'All fines for this borrower have been paid.')
            else:
                messages.error(request, 'No eligible fines to pay for this borrower.')
    
    if show_all:
        fines_qs = Fine.objects.all()
        if search_query:
            fines_qs = fines_qs.filter(
                Q(loan__borrower__card_no__icontains=search_query) |
                Q(loan__borrower__fname__icontains=search_query) |
                Q(loan__borrower__lname__icontains=search_query)
            )
        fines = fines_qs.values('loan__borrower__card_no', 'loan__borrower__fname', 'loan__borrower__lname').annotate(
            total_paid=Sum(Case(When(paid=True, then='fine_amt'))),
            total_unpaid=Sum(Case(When(paid=False, then='fine_amt'))),
        ).order_by('loan__borrower__card_no')
    else:
        fines_qs = Fine.objects.filter(paid=False)
        if search_query:
            fines_qs = fines_qs.filter(
                Q(loan__borrower__card_no__icontains=search_query) |
                Q(loan__borrower__fname__icontains=search_query) |
                Q(loan__borrower__lname__icontains=search_query)
            )
        fines = fines_qs.values('loan__borrower__card_no', 'loan__borrower__fname', 'loan__borrower__lname').annotate(
            total_unpaid=Sum('fine_amt'),
            num_unreturned=Count(Case(When(loan__date_in__isnull=True, then=1))),
            can_pay=Case(
                When(num_unreturned=0, then=True),
                default=False,
                output_field=BooleanField()
            )
        ).order_by('loan__borrower__card_no')
    
    return render(request, 'libraryapp/fines.html', {
        'fines': fines,
        'search_query': search_query,
        'show_all': show_all
    })
