from django import forms
from .models import Comment, Post

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','email','body']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'author', 'publish', 'status', 'tags']  # Include all fields you want in the form
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del post',
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Slug del post (URL-friendly)',
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe el contenido del post aquí...',
                'rows': 5,
            }),
            'author': forms.Select(attrs={
                'class': 'form-control',
            }),
            'publish': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
            }),
            # Assuming tags is handled by TaggableManager, it may require a different widget or handling
        }