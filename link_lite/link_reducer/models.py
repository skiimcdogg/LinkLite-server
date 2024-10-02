from django.db import models
from django.contrib.auth.models import User

class URL(models.Model):
    original_url = models.URLField()
    short_url = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.short_url
