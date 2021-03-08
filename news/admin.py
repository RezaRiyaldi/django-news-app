from django.contrib import admin

# Import class yang dibutuhkan untuk memodifikasi form pada User Admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

# Import helper timezone untuk mengeset waktu
from django.utils import timezone

# Import class model 
from .models import Category, News

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
   list_display = ('name', 'created_at')
   search_fields = ['name']

admin.site.register(Category, CategoryAdmin)


class NewsAdmin(admin.ModelAdmin):
   list_display = ('title', 'status', 'user', 'created_at')
   fields = ('title', 'content', 'excerpt', 'cover', 'status', 'categories')
   search_fields = ['title']
   list_filter = ('status',)

   # override method save_model untuk menyimpan data user dan published_at secara otomatis
   def save_model(self, request, obj, form, change):
      if not obj.user_id:
         obj.user = request.user

      if form.cleaned_data.get('status') == 1:
         # mengeset kolom "published_at" dengan nilai null jika status bernilai 1 (draft)
         obj.published_at = None
      else:
         # mengeset kolom "published_at" dengan tanggal dan waktu sekarang jika status bernilai 2 (Publish)
         obj.published_at = timezone.now()

      obj.save()
      
admin.site.register(News, NewsAdmin)


# Membuat Custom Form untuk form add user
class UserCreateForm(UserCreationForm):
   class Meta:
      model = User
      fields = ('username', 'first_name', 'last_name',)


# Membuat Custom Form untuk Form Update User
class UserUpdateForm(UserChangeForm):
   class Meta:
      model = User
      fields = ('username', 'first_name', 'last_name',)
   

# Mereset Custom User Form ke modul User Admin
class UserAdmin(UserAdmin):
   add_form = UserCreateForm
   form = UserUpdateForm
   prepopulated_fields = {
      'username' : ('first_name', 'last_name', )
   }

   add_fieldsets = (
      (None, {
         'classes': ('wide',),
         'fields': (
            'first_name', 'last_name', 'email', 'username', 'password1', 'password2', 
            ),
      }),
   )

   fieldsets = (
      (None, {
         'classes': ('wide',),
         'fields': (
            'first_name', 'last_name', 'email', 'username', 
         ),
      }),
   )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)