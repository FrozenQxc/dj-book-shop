from django.forms import ModelForm
from django import forms
from .models import Comment, Blog

class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ['title' ,'description', 'image','categories']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': "Комментарий"}


class Feedback(forms.Form):
    name = forms.CharField(label='Ваше имя', min_length=0, max_length=100)
    email = forms.EmailField(label='Email', min_length=0, max_length=100)
    problem = forms.ChoiceField(
        label='С какой проблемой вы столкнулись?', 
        choices=[('1', 'Проблема с оплатой'), ('2', 'Проблема с доставкой')]
    )
    description = forms.CharField(label='Опишите вашу проблему', min_length=0, max_length=100, widget=forms.Textarea(attrs={'rows': 5}))
