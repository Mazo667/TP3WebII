from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def post_list(request):
    post_list = Post.published.all()
    #Paginacion de 3 post por pagina
    paginator = Paginator(post_list,3)
    page_number = request.GET.get('page',1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        #Si page_number no es un entero
        posts = paginator.page(1)
    except EmptyPage:
        #Si page_number esta fuera de rango, obtenemos la ultima pagina con resultados
        posts = paginator.page(paginator.num_pages)

    return render(request,'post/list.html',{'posts':posts})

def post_detail(request, year,month,day,post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day)
    return render(request,'post/detail.html',{'post':post})