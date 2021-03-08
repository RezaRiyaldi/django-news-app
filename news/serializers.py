from rest_framework.serializers import ModelSerializer

# User Model
from django.contrib.auth.models import User

# Model lain
from .models import Category, News, Comment


# "Get List of Categories"
class CategoryListSerializer(ModelSerializer):
   class Meta:
      model = Category 
      fields = ('id', 'name', )

   
# "Get Detail of Categories"
class CategoryDetailSerializers(ModelSerializer):
   class Meta:
      model = Category
      fields = ('id', 'name', 'created_at', )


# Akan berelasi ke NewsSerializer
class UserSerializer(ModelSerializer):
   class Meta:
      model = User
      fields = ('id', 'first_name', 'last_name', )

   
class CommentListSerializer(ModelSerializer):
   class Meta:
      model = Comment
      fields = ('id', 'name', 'content', 'created_at', )


class CommentFormSerializer(ModelSerializer):
   class Meta:
      model = Comment
      fields = ('name', 'email', 'content', )


# Untuk API endpoint "Get List of News"
class NewsListSerializer(ModelSerializer):
   user = UserSerializer(read_only=True) # Relasi ke table user
   categories = CategoryListSerializer(many=True, read_only=True) # Relasi ke table Category

   class Meta:
      model = News
      fields = ('id', 'title', 'excerpt', 'user', 'categories', 'published_at')

   
# Untuk API endpoint "Get Detail of News"
class NewsDetailSerializer(ModelSerializer):
   user = UserSerializer(read_only=True) # relasi ke table user
   categories = CategoryListSerializer(many=True, read_only=True) # Relasi ke table Category
   comments = CommentListSerializer(many=True, read_only=True, source='comment_set') # Relasi ke table Comment
   
   class Meta:
      model = News
      fields = ('id', 'title', 'excerpt', 'content', 'cover', 'published_at', 'user', 'categories', 'comments',)