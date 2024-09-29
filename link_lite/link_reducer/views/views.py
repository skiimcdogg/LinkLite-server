from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from ..models import URL
from ..services.UrlShortenService import UrlShortenService
from ..presenter.UrlPresenter import UrlPresenter
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import IsAuthenticated

@ensure_csrf_cookie
def get_csrf_token(request):
    print(request)
    return JsonResponse({'detail': 'CSRF cookie set.'})

def shorten_url(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        user = request.user if request.user.is_authenticated else None

        short_url = UrlShortenService.create_short_url(original_url, user)

    return HttpResponse(f"Short URL created -> {short_url}")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_urls_from_user(request):
    user = request.user

    if not user.is_authenticated():
        return HttpResponse("You have to be connected", status=403)
    
    user_url_list = UrlPresenter.user_urls(user)
    return JsonResponse({"urls": user_url_list}, safe=False)

def redirect_url(request, short_url):
    try:
        url = get_object_or_404(URL, short_url=short_url)
        redirect(url.original_url)

    except URL.DoesNotExist:
        return HttpResponse("L'URL courte n'existe pas.", status=404)
    
    except Exception as e:
        return HttpResponse(f"Une erreur est survenue : {str(e)}", status=500)
    
@login_required
def delete_url(request, short_url):
    if request.method == 'DELETE':
        try:
            url = get_object_or_404(URL, short_url=short_url, user=request.user)
            
            url.delete()
            return JsonResponse({'detail': 'URL supprimée avec succès.'}, status=200)
        except URL.DoesNotExist:
            return JsonResponse({'error': 'URL non trouvée ou vous n\'êtes pas autorisé à la supprimer.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Une erreur est survenue : {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Méthode non autorisée.'}, status=405)
