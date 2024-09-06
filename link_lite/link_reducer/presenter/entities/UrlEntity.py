from dataclasses import dataclass
from datetime import datetime

@dataclass
class UrlEntity:
    id: int
    short_url: str
    original_url: str
    created_at: datetime

    def to_dict(self):
        return {
            "id": self.id,
            "short_url": self.short_url,
            "original_url": self.original_url,
            "created_at": datetime.timestamp(self.created_at),
        }
    