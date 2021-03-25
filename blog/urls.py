from django.urls import path
from .views import (
    PostListView,
    post_detail,
    post_search,
    PostLikes,
)

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name="post-list"),
    path('post/<slug>/', post_detail, name="post-detail"),
    path('<pk>/post/likes/', PostLikes.as_view(), name="post-likes"),
    path('post-search/', post_search, name="post-search"),
]
