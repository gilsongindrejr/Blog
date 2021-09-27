from django.urls import path

from .views import PostListView, post_detail, post_share

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', post_detail, name='detail'),
    path('<int:post_id>/share/', post_share, name='share'),
]
