from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'post/list.html'

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