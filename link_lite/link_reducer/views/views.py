from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from ..models import URL
from ..services.UrlShortenService import UrlShortenService
from ..presenter.UrlPresenter import UrlPresenter

def shorten_url(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        user = request.user if request.user.is_authenticated() else None

        short_url = UrlShortenService.create_short_url(original_url, user)

    return HttpResponse(f"Short URL created -> {short_url}")

def get_all_urls_from_user(request):
    user = request.user

    if not user.is_authenticated():
        return HttpResponse("You have to be connected", status=403)
    
    user_url_list = UrlPresenter.user_urls(user)
    return JsonResponse({"urls": user_url_list}, safe=False)

def redirect_url(request, short_url):
    url = get_object_or_404(URL, short_url=short_url)
    redirect(url.original_url)
