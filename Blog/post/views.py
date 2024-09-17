from django.shortcuts import render
from .models import Post

def post_list(request):
    posts = Post.published.all()
    return render(request,'post/list.html',{'posts':posts})

def post_detail(request, id):
    try:
        post = Post.published.get(id=id)
    except Post.DoesNotExist:
        raise Http404("Post no encontrado")
    return render(request,'post/detail.html',{'post':post})