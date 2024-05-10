from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Blog, Category
from .forms import BlogForm
from django.shortcuts import render
from .forms import Feedback
from django.contrib.auth import logout 


def home(request):
    blogs = Blog.objects.order_by('-date')[:5]
    return render(request, 'main/home.html', {'blogs': blogs}
)

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

def register(request):
    if request.method == 'GET':
        return render(request, 'main/register.html', {'form': UserCreationForm()})
    else:
        try:
            if request.POST['password1'] == request.POST['password2']:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('account') 
            else:
                return render(request, 'main/register.html', {'form': UserCreationForm(), 'error': 'Пароли не совпадают'})
        except IntegrityError:
            return render(request, 'main/register.html', {'form': UserCreationForm(), 'error': 'Имя пользователя уже существует'})
        except KeyError:
            return render(request, 'main/signup_user.html', {'form': UserCreationForm(), 'error': 'Все поля должны быть заполнены'})



def login_user(request):
    if request.method == 'GET':
        return render(request, 'main/loginUser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('account')
        else:
            return render(request, 'main/loginUser.html', {'form': AuthenticationForm(), 'error': 'Имя пользователя или пароль неверны'})      


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')



def account(request):
    blogs = Blog.objects.filter(user=request.user)
    return render(request, 'main/account.html')

def account(request):
    blogs = Blog.objects.filter(user=request.user)
    return render(request, 'main/account.html', {'blogs':blogs})


def createBlog(request):
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
    return render(request, 'main/createBlog.html', {'form': form})


def changeBlog(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            if 'image' in request.FILES:
                blog.image = request.FILES['image']
            form.save()
            return redirect('account')
        else:
            return render(request, 'main/changeBlog.html', {'blog': blog, 'form': form, 'error': 'Ошибка'})
    else:
        form = BlogForm(instance=blog)
        return render(request, 'main/changeBlog.html', {'blog': blog, 'form': form})


def deleteBlog(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    if request.method == 'POST':
        blog.delete()
        return redirect('account')


def detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'main/detail.html', {'blog': blog})


def blog(request):
    categories = Category.objects.all() 
    blogs = Blog.objects.all() 
    if request.method == 'POST': 
        category_id = request.POST.get('category_id') 
        category = get_object_or_404(Category, id=category_id) 
        blogs = Blog.objects.filter(categories=category) 
    return render(request, 'main/blog.html', {'categories': categories, 'blogs':blogs})

