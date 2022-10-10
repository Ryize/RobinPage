from django.db import models


class CopySite(models.Model):
    hash_text = models.CharField(max_length=512, verbose_name="Хеш")
    url = models.URLField(verbose_name="URL")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = "Скопированный сайт"
        verbose_name_plural = "Скопированные сайты"
