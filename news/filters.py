from django_filters import rest_framework as filters
from .models import News

class NewsFilter(filters.FilterSet):
   # custom filter berdasarkan nama kategori
   categories = filters.CharFilter(field_name="categories__name", lookup_expr='exact')

   # custom filter tanggal publish news
   # berdasarkan range tanggal dari parameter published_after & published before
   published = filters.DateFromToRangeFilter(field_name="published_at")

   class Meta:
      model = News
      fields = ['title', 'categories', 'published']