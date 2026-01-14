from rest_framework import viewsets, filters
from .models import Author, Category, Post, Comment
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from .serializers import AuthorSerializer,CategorySerializer,PostSerilaizer,CommentSerializer

class AuthorViewset(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
    @action(detail=True, methods=['get'])
    def posts(self, request, pk=""):
        author = self.get_object()
        posts = Post.objects.filter(author=author)
        serializer = PostSerilaizer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    
class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]  # enable search
    search_fields = ['title']
    
class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerilaizer
    
    
    def get_queryset(self):
        queryset = Post.objects.all()
        is_published = self.request.query_params.get('is_published')
        if is_published is not None:
            queryset = queryset.filter(is_published=is_published.lower() == 'true')
        
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author_id=author)
        
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(categories__id=category)   
            
        return queryset
    
    # STEP 2: Publish a post
    @action(detail=True, methods=['patch'])
    def publish(self, request, pk=None):
        post = self.get_object()     # get post by id
        post.is_published = True     # mark as published
        post.save()                  # save to DB
        return Response({
            "message": "Post published successfully"
        })
        
    # STEP 3: List only published posts
    @action(detail=False, methods=['get'])
    def published(self, request):
        posts = Post.objects.filter(is_published=True)
        serializer = self.get_serializer(
            posts,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data) 
    
    @action(detail=True, methods=['post'])
    def comments(self, request, pk=None):
        post = self.get_object()   # get post by id
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(post=post)  # attach comment to post
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
    
    
    
class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer 
     
    
    #List pending comments
    @action(detail=False, methods=['get'])
    def pending(self, request):
        comments = Comment.objects.filter(is_approved=False)
        serializer = self.get_serializer(
            comments,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)  
    
    @action(detail=True, methods=['patch'])
    def approve(self, request, pk=None):
        comment = self.get_object()  # get comment by ID
        comment.is_approved = True   # mark as approved
        comment.save()               # save changes
        return Response({
            "message": "Comment approved successfully"
            })       


