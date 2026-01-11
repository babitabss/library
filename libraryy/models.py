from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
class Book(models.Model):
    GENRE_CHOICES = [
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Mystery', 'Mystery'),
        ('Science', 'Science'),
        ('Biography', 'Biography'),
        
    ]
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True, blank= True, null = True)
    published_date = models.DateField()
    genre = models.CharField(max_length=20, choices= GENRE_CHOICES)
    is_available = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        if self.published_date > timezone.now().date():
            raise ValidationError("Published date cannot be in the future.")

    def __str__(self):
        return self.title