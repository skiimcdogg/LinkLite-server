import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import IsAuthenticated
from ..models import URL
from ..services.UrlShortenService import UrlShortenService
from ..presenter.UrlPresenter import UrlPresenter
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set.'})

def shorten_url(request):
    if request.method == 'POST':
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return JsonResponse({"error": "Authorization header missing"}, status=401)
        
        try:
            token_str = auth_header.split(' ')[1]
            token = AccessToken(token_str)
            user_id = token['user_id']
            user = User.objects.get(id=user_id)
        except Exception as e:
            return JsonResponse({"error": "Invalid or expired token"}, status=401)
        original_url = json.loads(request.body)
        short_url = UrlShortenService.create_short_url(original_url["originalUrl"], user)
    if isinstance(short_url, JsonResponse):
        return short_url
    return JsonResponse({
        "result": short_url
    }, safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_urls_from_user(request):
    user = request.user

    if not user.is_authenticated:
        return HttpResponse("You have to be connected", status=403)
    
    user_url_list = UrlPresenter.user_urls(user)
    return JsonResponse({"urls": user_url_list}, safe=False)

def redirect_url(request, short_url):
    try:
        short_url_code = short_url.split("/")[-1]
        url = get_object_or_404(URL, short_url=short_url_code)
        return redirect(url.original_url)

    except URL.DoesNotExist:
        return HttpResponse("L'URL courte n'existe pas.", status=404)
    
    except Exception as e:
        return HttpResponse(f"Une erreur est survenue : {str(e)}", status=500)
    
def delete_url(request, short_url):
    if request.method == 'DELETE':
        try:
            url = get_object_or_404(URL, short_url=short_url)
            url.delete()
            return JsonResponse({'detail': 'URL deleted successfully.'}, status=200)
        except URL.DoesNotExist:
            return JsonResponse({'error': 'URL not found or you\'re not auhorized.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'An error occured : {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)
