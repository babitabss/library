
from .models import Author, Category, Post, Comment
from rest_framework import serializers

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        
class PostSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'tittle',
            'content',
            'author',
            'categories',
            'is_published',
            'created_at',
            'updated_at',
            'comments'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # show only approved comments
        data['comments'] = CommentSerializer(
            instance.comments.filter(is_approved=True),
            many=True
        ).data
        return data
    
    def validate_title(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Title must be at least 10 characters")
        return value
        
        
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category    
        fields = '__all__'   
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author_name', 'content', 'is_approved' ,'created_at'] 
        read_only_fields = ['is_approved', 'created_at'] 
        
    def create(self, validated_data):
        post = validated_data.get('post')
        if not post.is_published:
            raise serializers.ValidationError("Cannot add comment to an unpublished post")
        return super().create(validated_data)                  