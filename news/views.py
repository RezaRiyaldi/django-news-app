# class untuk membuat view
from django.http import Http404
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

# Authentication rest API
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Local
from .models import Category, News, Comment

# class serializers dari aplikasi newsapp
from .serializers import CategoryListSerializer, CategoryDetailSerializers, NewsListSerializer, NewsDetailSerializer, CommentFormSerializer

# Fitur Filtering
from .filters import NewsFilter

# package untuk menambah judul dan deskripsi pada dokument API
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator


# View untuk API endpoint "Get All Categories"
# /api/category
@method_decorator(name="get", decorator=swagger_auto_schema(operation_id='Get List of Categories', operation_description="Return a paginated array of Categories."))
class CategoryListView(ListAPIView):
   # Mengeset class serializers
   serializer_class = CategoryListSerializer
   queryset = Category.objects.all()

   # Fitur filtering, searching & ordering
   filter_backends = (
      DjangoFilterBackend,
      SearchFilter,
      OrderingFilter,
   )

   # Filtering
   filter_fields = ['name']

   # Searching
   search_fields = ['name']

   # Ordering
   ordering_fields = ['name', 'created_at']

   # Default untuk Ordering
   ordering = ['created_at']

   # Authentication
   permission_classes = (IsAuthenticated,)
   authentication_classes = [TokenAuthentication]


# View untuk API endpoint "Get Detail of Categories"
# /api/category/:id
@method_decorator(name="get", decorator=swagger_auto_schema(operation_id='Get Detail of Categories', operation_description="Return a single Category by id."))
class CategoryDetailView(RetrieveAPIView):
   # Set class serializers
   serializer_class = CategoryDetailSerializers
   queryset = Category.objects.all()

   # Authentication
   permission_classes = (IsAuthenticated,)
   authentication_classes = [TokenAuthentication]


# View untuk API endpoint "Get List of News"
# api/news
@method_decorator(name="get", decorator=swagger_auto_schema(operation_id='Get List of News', operation_description="Return a paginated array of News."))
class NewsListView(ListAPIView):
   serializer_class = NewsListSerializer
   # Ambil data news dengan status `published`
   queryset = News.objects.is_published()

   filter_backends = (
      DjangoFilterBackend,
      SearchFilter,
      OrderingFilter
   )

   # Fitur Filtering
   filterset_class = NewsFilter

   # Fitur Searching
   search_fields = ['title']

   # Fitur Ordering
   ordering_fields = ['title', 'created_at']

   # Default untuk Fitur Ordering
   ordering = ['created_at']

   # Authentication
   permission_classes = (IsAuthenticated,)
   authentication_classes = [TokenAuthentication]


# View untuk API endpoint "Get Detail of News"
# api/news/:id
@method_decorator(name="get", decorator=swagger_auto_schema(operation_id='Get Detail of News', operation_description="Return a single News by id."))
class NewsDetailView(RetrieveAPIView):
   serializer_class = NewsDetailSerializer
   # Ambil data news dengan status `published`
   queryset = News.objects.is_published()

   # Authentication
   permission_classes = (IsAuthenticated,)
   authentication_classes = [TokenAuthentication]


# View untuk API endpoint "Create New Comment on News"
# api/news/:id/comment
@method_decorator(name="post", decorator=swagger_auto_schema(operation_id='Create New Comment on News', operation_description="Create a new comment on news."))
class NewsCreateCommentView(CreateAPIView):
   serializer_class = CommentFormSerializer
   queryset = Comment.objects.all()

   # Override method perform_create untuk mengambil news_id dari parameter url API point
   def perform_create(self, serializer):
      news_id = self.kwargs['pk']
      try:
         news = News.objects.get(pk=news_id)
         serializer.save(news_id=news_id)
      except News.DoesNotExist:
         raise Http404