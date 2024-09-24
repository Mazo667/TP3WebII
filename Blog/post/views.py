from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm, PostForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages


def post_share(request, post_id):
    post = get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (f"{cd['name']} ({cd['email']}) "
                       f"recomienda que leas {post.title}")
            message = (f"Lee {post.title} en {post_url}\n\n"
                       f"{cd['name']} comentario: {cd['comments']}")
            send_mail(subject=subject,message=message,from_email=None,recipient_list=[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request,'post/share.html',{'post':post,'form':form,'sent':sent})

@login_required
def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
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

    return render(request,'post/list.html',{'posts':posts,'tag':tag})

def post_detail(request, year,month,day,post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    #List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
    tags__in=post_tags_ids
    ).exclude(id=post.id)
    similar_posts = similar_posts.annotate(
    same_tags=Count('tags')
    ).order_by('-same_tags', '-publish')[:4]

    return render(request,'post/detail.html',{'post':post,'comments':comments,'form':form,'similar_posts':similar_posts})

@require_POST
def post_comment(request,post_id):
    post = get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request,'post/comment.html',{'post':post,'form':form,'comment':comment})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user == post.author:
        post.delete()
        messages.success(request, "Post eliminado correctamente.")
        return redirect('post:post_list') 
    else:
        messages.error(request, "No tienes permiso para eliminar este post.")
        return redirect('post:post_detail', post_id=post.id)
    
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        messages.error(request, "No tienes permiso para editar este post.")
        return redirect('post:post_detail', post_id=post.id)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post actualizado correctamente.")
            return redirect('post:post_list') 
    else:
        form = PostForm(instance=post)

    return render(request, "post/edit_post.html", {'form': form, 'post': post})

@login_required
def confirm_delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        messages.error(request, "No tienes permiso para eliminar este post.")
        return redirect('post:post_detail', post_id=post.id)

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post eliminado correctamente.")
        return redirect('post:post_list') 

    return render(request, "post/confirm_delete.html", {'post': post})

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # Create a post instance but don't save it yet
            post.author = request.user  # Set the author to the logged-in user
            post.save()  # Save the post instance to the database
            messages.success(request, "Post creado correctamente.")
            return redirect('post:post_list')  # Redirect to the post list or another page
    else:
        form = PostForm()  # Create an empty form for GET requests

    return render(request, "post/create_post.html", {'form': form})