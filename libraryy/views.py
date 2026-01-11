from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        #First, get all books from the database
        queryset = super().get_queryset()
        
        # Get 'genre' value from URL (example: ?genre=Fiction)
        #If user doesnot send genre, this will be none 
        genre = self.request.query_params.get('genre')
        
        # Get 'is_available' value from URL (example: ?is_available=true)
        # If user does not send this, it will be None
        is_available = self.request.query_params.get('is_available')
        
        # If user has sent genre in the UR
        if genre:
            
            # Filter books to keep only books of that genre
            queryset = queryset.filter(genre=genre)
        
        # If user has sent availability info in the URL
        if is_available:
            # Filter books to keep only available / unavailable books
            queryset = queryset.filter(is_available=is_available)
        # Finally, return the filtered list of books
        return queryset
