from django.urls import path
from .views import CategoryListView, CategoryDetailView, NewsListView, NewsDetailView, NewsCreateCommentView

urlpatterns = [
   # Categories
   path('category/', CategoryListView.as_view(), name='api-category-list'),
   path('category/<int:pk>/', CategoryDetailView.as_view(), name='api-category-detail'),

   # News
   path('news', NewsListView.as_view(), name='api-news-list'),
   path('news/<int:pk>/comment/', NewsCreateCommentView.as_view(), name='api-news-create-comment'),
   path('news/<int:pk>/', NewsDetailView.as_view(), name='api-news-detail'),

]