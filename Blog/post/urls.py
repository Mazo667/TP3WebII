from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
   # path('', views.PostListView.as_view(), name='post_list'),
    path('',views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/',views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/',views.post_share, name='post_share'),
    path('<int:post_id>/comment/',views.post_comment, name="post_comment"),
    path('<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('<int:post_id>/confirm-delete/', views.confirm_delete_post, name='confirm_delete_post'),
    path('post/create/', views.create_post, name='create_post'),
]