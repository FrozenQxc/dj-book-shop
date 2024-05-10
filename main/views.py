from django.shortcuts import render
from .forms import Feedback
from django.contrib.auth import logout 

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Blog, Category
from .forms import BlogForm



def home(request):
    return render(request, 'main/base.html')
def pool(request):
    data = None
    problem_choices = {'1': 'Проблема с оплатой', '2': 'Проблемы с доставкой'}
    
    if request.method == 'POST':
        form = Feedback(request.POST)
        if form.is_valid():
            problem = form.cleaned_data['problem']
            data = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'problem': problem_choices.get(problem, 'Неизвестная проблема'),
                'description': form.cleaned_data['description']
            }
    else:
        form = Feedback()
    
    return render(request, 'main/pool.html', {'form': form, 'data': data})


@login_required    
def account(request):
    blogs = Blog.objects.filter(user=request.user)
    return render(request, 'main/account.html', {'blogs':blogs})

@login_required    
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.user = request.user
            new_blog.image = request.FILES['image'] # имя поля для загрузки изображения
            new_blog.save()
            return redirect('account')
    else:
        form = BlogForm()
    return render(request, 'blog/create_blog.html', {'form': form})


@login_required    
def change_blog(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            if 'image' in request.FILES:
                blog.image = request.FILES['image']
            form.save()
            return redirect('account')
        else:
            return render(request, 'blog/change_blog.html', {'blog': blog, 'form': form, 'error': 'Ошибка'})
    else:
        form = BlogForm(instance=blog)
        return render(request, 'blog/change_blog.html', {'blog': blog, 'form': form})


@login_required    
def delete_blog(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    if request.method == 'POST':
        blog.delete()
        return redirect('account')


def detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blog/detail.html', {'blog': blog})

def blog(request):
    categories = Category.objects.all() 
    blogs = Blog.objects.all() 
    if request.method == 'POST': 
        category_id = request.POST.get('category_id') 
        category = get_object_or_404(Category, id=category_id) 
        blogs = Blog.objects.filter(categories=category) 
    return render(request, 'blog/blog.html', {'categories': categories, 'blogs':blogs})

# Вход в аккаунт 
def login_user(request):
    if request.method == 'GET':
        return render(request, 'auth/login.html', {'form': AuthenticationForm()})
    else:
        # Аутентификация пользователя
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            return render(request, 'auth/login.html', {'form': AuthenticationForm(), 'error': 'Имя пользователя или пароль неверны'})
# Регистрация
def register(request):
    if request.method == 'GET':
        return render(request, 'auth/register.html', {'form': UserCreationForm()})
    else:
        try:
            if request.POST['password1'] == request.POST['password2']:
                # если пароли совпадают, создать нового пользователя
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')  
            else:
                return render(request, 'auth/register.html', {'form': UserCreationForm(), 'error': 'Пароли не совпадают'})
        except IntegrityError:
            # если имя пользователя уже существует, вернуть ошибку
            return render(request, 'auth/register.html', {'form': UserCreationForm(), 'error': 'Имя пользователя уже существует'})
        except KeyError:
            return render(request, 'auth/register.html', {'form': UserCreationForm(), 'error': 'Все поля должны быть заполнены'})
# Выход из аккаунта
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
