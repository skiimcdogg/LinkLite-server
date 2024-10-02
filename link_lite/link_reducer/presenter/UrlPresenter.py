from ..data.repositories.UrlRepository import UrlRepository
from .entities.UrlEntity import UrlEntity


class UrlPresenter:

    @staticmethod
    def user_urls(user):
        urls_data = UrlRepository.get_all_url_from_user(user)

        url_entities = [
            UrlEntity(url.id, url.short_url, url.original_url, url.created_at)
            for url in urls_data
        ]

        return [url_entity.to_dict() for url_entity in url_entities]