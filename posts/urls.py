from django.conf.urls import url
from posts import views
from . import views

urlpatterns = [
    url(r'^$', views.posts_list, name='list'),
    url(r'^create/$', views.posts_create, name="posts_create"),
    url(r'^create/try/$', views.posts_sudocreate, name= "posts_sudocreate"),
    url(r'^(?P<slug>[\w-]+)$', views.posts_detail, name="detail"),
    url(r'^(?P<slug>[\w-]+)/edit/$', views.posts_update, name='update'),
    url(r'^update/try/$', views.posts_sudoupdate, name= "posts_sudoupdate"),
    url(r'^(?P<slug>[\w-]+)/delete/$', views.posts_delete),
    url(r'^search/$', views.posts_search, name= "posts_search")
]
