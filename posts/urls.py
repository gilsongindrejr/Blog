from django.urls import path

from .views import post_list, post_detail, post_share

app_name = 'blog'

urlpatterns = [
    path('', post_list, name='index'),
    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', post_detail, name='detail'),
    path('<int:post_id>/share/', post_share, name='share'),
]
