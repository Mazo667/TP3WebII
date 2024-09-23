from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

class PublishedManager(models.Manager):
    def get_queryset(self):
        return (super().get_queryset().filter(status=Post.Status.PUBLISHED))


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        unique_for_date='publish')
    body = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )

    objects = models.Manager() # El manejador por defecto
    published = PublishedManager() # El manejador customizado

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return f'{self.title}: {self.body} [{self.slug}] / ({self.publish}). STATUS: {self.status}'
    
    def get_absolute_url(self):
        return reverse('post:post_detail', args=[
            self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug]
            )
    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]

    def __str__(self):
        return f'Comentado por {self.name} en {self.post}'