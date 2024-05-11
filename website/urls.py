from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),

    # Шапка
    path('pool/', pool, name='pool'),
    path('about/', about, name='about'),  
    path('video/', videopost, name='video'),


    # Аутентификация 
    path('logout/', logout_user, name='logout_user'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login_user'),

    # Аккаунт   
    path('account/', account, name='account'),
    path('account/create-blog/', create_blog, name='create_blog'),
    path('account/<int:blog_pk>/delete/', delete_blog, name='delete_blog'),  # Добавлена косая черта в конце
    path('account/<int:blog_pk>/change/', change_blog, name='change_blog'),  # Добавлена косая черта в конце

    path('blog/', include('main.urls')),
    path('blog/', blog, name='blog'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
