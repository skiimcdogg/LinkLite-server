from ..data.repositories.UrlRepository import UrlRepository
from ..utils import generate_short_code


class UrlShortenService:

    @staticmethod
    def create_short_url(original_url, user=None):
        short_code = generate_short_code()

        if UrlRepository.exists_by_short_code(short_code):
            short_code = generate_short_code()

        url = UrlRepository.save(original_url, short_code, user)

        return f"http://localhost:8000/{short_code}" # [ ] Remplacer par l'url env de l'app