from django.http import HttpResponse
from django.shortcuts import render

def shorten_url(request):
    return HttpResponse("Hello")

def get_all_urls(request):
    return HttpResponse("Hello")
