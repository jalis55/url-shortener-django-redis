from django.db import models

# Create your models here.
class URL(models.Model):
    original_url = models.URLField(max_length=200)
    short_code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"