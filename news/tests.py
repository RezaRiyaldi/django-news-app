# module untuk testing
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

# Membuat data dummy
from .models import Category, News
from .serializers import CategoryDetailSerializers, NewsDetailSerializer


# Create your tests here.
class NewsAppApiTest(TestCase):
   """Membuat data dummy untuk Testing"""

   def setUp(self):
      self.client = APIClient()
      self.user = User.objects.create_user(username='usertest', password='12345')
      token = Token.objects.get(user__username=self.user.username)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      self.category = Category.objects.create(name='Category Test')

      dummy_image = (
         b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
         b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
         b'\x02\x4c\x01\x00\x3b'
      )
      cover = SimpleUploadedFile('small.gif', dummy_image, content_type='image/gif')

      self.news = News.objects.create(
         title = 'News Test',
         excerpt = 'Short Content',
         content = 'Long content with sample text',
         cover = cover,
         status = News.NewsStatus.published,
         user = self.user
      )

   """Testing untuk API endpoint Get Category List"""

   def tes_can_get_category_list(self):
      response = self.client.get(reverse('api-category-list'))
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   """Testing untuk API endpoint Get Category Detail"""

   def test_can_get_category_detail(self):
      response = self.client.get(reverse('api-category-detail', args=[self.category.id]))
      category = Category.objects.get(pk=self.category.id)
      serializer = CategoryDetailSerializers(category)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(response.data, serializer.data)

   """Testing untuk APi endpoint Get Category Detail"""
   """Status Gagal: ID tidak valid"""

   def test_get_cannot_category_detail(self):
      res = self.client.get(reverse('api-category-detail', args=[999]))
      self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

   """Testing untuk API endpoint Get News List"""

   def tes_can_get_news_list(self):
      """Can get News List"""
      response = self.client.get(reverse('api-news-list'))
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   """Testing untuk API endpoint Get News List"""
   
   def test_can_get_news_detail(self):
      response = self.client.get(reverse('api-news-detail', args=[self.news.id]))
      news = News.objects.is_published().get(pk=self.news.id)
      serializer = NewsDetailSerializer(news)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(response.data.keys(), serializer.data.keys())

   """Testing untuk API endpoint Get News Detail"""
   """Status Gagal: ID tidak valid"""

   def test_cannot_get_news_detail(self):
      response = self.client.get(reverse('api-news-detail', args=[999]))
      self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

   """Testing untuk API endpoint Post News Create Comment"""

   def test_can_post_news_create_comment(self):
      payload = {
         'name': 'Commenter',
         'email': 'commenter@test.com',
         'content': 'Another Comment Test'
      }
      response = self.client.post(
         reverse('api-news-create-comment', args=[self.news.id]),
         payload
      )
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)

   """Testing untuk API endpoint post News Create Comment"""
   """Status Gagal: Payload tidak valid"""

   def test_cannot_post_news_create_comment(self):
      payload = {
         'name': 'commenter',
         'email': '',
         'content':''
      }
      response = self.client.post(
         reverse('api-news-create-comment', args=[self.news.id]),
         payload
      )
      self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

   """Menghapus data image dummy untuk Testing"""

   def tearDown(self):
      self.news.cover.delete(False)