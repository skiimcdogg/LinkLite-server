from django.http import JsonResponse
from ...models import URL


class UrlRepository:
    def get_all_url_from_user(user):
        urls = URL.objects.filter(user=user)

        return urls

    @staticmethod
    def save(original_url, short_code, user=None):
        url_object = URL.objects.filter(original_url=original_url).first()
        if url_object:
            return JsonResponse({
                "result": f"http://localhost:8000/{url_object.short_url}",
                "details": "Url already exists"
            }, status=409)
        return URL.objects.create(original_url=original_url, short_url=short_code, user=user)
    
    @staticmethod
    def exists_by_short_code(short_code):
        return URL.objects.filter(short_url=short_code).exists()
    
