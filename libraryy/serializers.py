from rest_framework import serializers
from .models import Book
from django.utils import timezone

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'

    def validate_published_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Published date cannot be in the future.")
        return value
