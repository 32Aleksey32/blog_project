from django.urls import path

from .views import DislikePost, LikePost, PostCreate, PostDelete, PostDetail, PostEdit, PostList

urlpatterns = [
    path('', PostList.as_view(), name='index'),
    path('post/create/', PostCreate.as_view(), name='post-create'),
    path('post/<int:post_id>/', PostDetail.as_view(), name='post-detail'),
    path('post/<int:post_id>/edit/', PostEdit.as_view(), name='post-edit'),
    path('post/<int:post_id>/delete/', PostDelete.as_view(), name='post-delete'),
    path('like/<int:post_id>/', LikePost.as_view(), name='post-like'),
    path('dislike/<int:post_id>/', DislikePost.as_view(), name='post-dislike'),
]
