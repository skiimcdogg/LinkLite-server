from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from ..models import URL

def shorten_url(request):
    return HttpResponse("Hello")

def get_all_urls(request):
    return HttpResponse("Hello")

def redirect_url(request, short_url):
    url = get_object_or_404(URL, short_url=short_url)
    redirect(url.original_url)
