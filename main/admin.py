from django.contrib import admin
from .models import Blog, Category,Carousel, Comment
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'description','image', 'date' , 'user' )
    
admin.site.register(Blog,BlogAdmin)
admin.site.register(Category)
admin.site.register(Carousel)
admin.site.register(Comment)
