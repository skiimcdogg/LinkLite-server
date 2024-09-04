from dataclasses import dataclass
import datetime
from django.contrib.auth.models import User

@dataclass
class UrlData:
    id: int
    original_url: str
    short_url: str
    created_at: datetime.datetime
    user: User