from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

class Book(models.Model):
    isbn = models.CharField(max_length=13, primary_key=True, validators=[MinLengthValidator(10), MaxLengthValidator(13)])
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField('Author', related_name='books')
    
    def __str__(self):
        return f"{self.title} ({self.isbn})"

class Author(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Borrower(models.Model):
    card_no = models.CharField(max_length=10, primary_key=True)
    ssn = models.CharField(max_length=9, unique=True, validators=[MinLengthValidator(9), MaxLengthValidator(9)])
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.fname} {self.lname} ({self.card_no})"

class BookLoan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    date_out = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    date_in = models.DateField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = self.date_out + timedelta(days=14)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Loan {self.loan_id}: {self.book} borrowed by {self.borrower}"

class Fine(models.Model):
    loan = models.ForeignKey(BookLoan, on_delete=models.CASCADE)
    fine_amt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Fine for {self.loan}: ${self.fine_amt} ({'Paid' if self.paid else 'Unpaid'})"
