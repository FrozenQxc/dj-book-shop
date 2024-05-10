from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
       
    def __str__(self):
        return self.name
    
class Blog(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to='main/images', verbose_name="Изображение")
    url = models.URLField(blank=True, verbose_name="URL")
    date = models.DateField(default=timezone.now, verbose_name="Дата")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, verbose_name="Пользователь")
    categories = models.ManyToManyField(Category, related_name='blogs', blank=True, verbose_name="Категории")



