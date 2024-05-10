from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime

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

 
class Comment(models.Model):
    text = models.TextField(verbose_name="Текст комментария")
    date = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name="Дата комментария")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор комментария")
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="Статья комментария")

    def __str__(self):
        return 'Комментарий %d %s к %s' % (self.id, self.author, self.post)

    class Meta:
        db_table = "Comment"
        ordering = ["-date"]
        verbose_name = "Комментарии к статье блога"
        verbose_name_plural = "Комментарии к статьям блога"