from django.db import models
from django.contrib.auth.models import User

# untuk generate token user
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.
class Category(models.Model):
   name = models.CharField(max_length=100)
   created_at = models.DateTimeField(auto_now_add=True)
   update_at = models.DateTimeField(auto_now=True)

   class Meta:
      db_table = 'category'
      verbose_name_plural = "Category"

   def __str__(self):
      return self.name

# Membuat Custom Manager
class NewsManager(models.Manager):
   # Method untuk memfilter news/berita yang hanya berstatus `published`
   def is_published(self):
      return super().get_queryset().filter(status=News.NewsStatus.published)


# Model News
class News(models.Model):
   class NewsStatus(models.IntegerChoices):
      draft = 1
      published = 2

   title = models.CharField(max_length=255)
   cover = models.ImageField(upload_to='images')
   content = models.TextField()
   excerpt = models.TextField()
   status = models.IntegerField(choices=NewsStatus.choices)
   published_at = models.DateTimeField(null=True)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   # Set relasi ke table user dan category
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   categories = models.ManyToManyField(Category)

   # Menambahkan NewsManager
   objects = NewsManager()

   class Meta:
      db_table = 'news'
      verbose_name_plural = 'News'

   def __str__(self):
      return self.title
   

class Comment(models.Model):
   name = models.CharField(max_length=100)
   email = models.EmailField()
   content = models.TextField()
   created_at = models.DateField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   # Relasi ke table News
   news = models.ForeignKey(News, on_delete=models.CASCADE)

   class Meta:
      db_table = 'comment'


# Generate token secara otomatis
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
   if created:
      Token.objects.create(user=instance)