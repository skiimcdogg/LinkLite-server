from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from ..models import URL
from ..services.UrlShortenService import UrlShortenService

def shorten_url(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        user = request.user if request.user.is_authenticated() else None

        short_url = UrlShortenService.create_short_url(original_url, user)

    return HttpResponse(f"Short URL created -> {short_url}")

def get_all_urls(request):
    return HttpResponse("Hello")

def redirect_url(request, short_url):
    url = get_object_or_404(URL, short_url=short_url)
    redirect(url.original_url)
