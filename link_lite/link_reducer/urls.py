from django.urls import path
from . import views

urlpatterns = [
    path('shorten-url', views.shorten_url, name='shorten_url'),
    path('list-user-urls', views.get_all_urls, name='list_urls'),
]