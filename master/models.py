from django.db import models
from common.models import BaseModel

class Keyword(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Keyword Name")
    code = models.CharField(max_length=100, unique=True, verbose_name="Keyword Code")
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Keyword"
        verbose_name_plural = "Keywords"

    def __str__(self):
        return self.name

class Counter(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Counter Name")
    keyword = models.ForeignKey(
        Keyword,
        null=True,
        blank=True,
        editable=True,
        default='',
        on_delete=models.CASCADE,
        related_name='keyword_counter'
    )
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Counter"
        verbose_name_plural = "Counters"

    def __str__(self):
        return self.name
