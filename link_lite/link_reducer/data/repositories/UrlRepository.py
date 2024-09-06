from ...models import URL


class UrlRepository:
    def get_all():
        pass

    @staticmethod
    def save(original_url, short_code, user=None):
        return URL.objects.create(original_url=original_url, short_url=short_code, user=user)
    
    @staticmethod
    def exists_by_short_code(short_code):
        return URL.objects.filter(short_url=short_code).exists()
    
