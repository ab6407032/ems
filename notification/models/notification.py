from django.db import models
from tinymce import models as tinymce_models

USUAGE = (
    ('welcome', 'Welcome'),
    ('password_change', 'Password Change'),
    ('otp', 'Otp'),
    ('oth', 'Others')
)


class Template(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    subject = models.CharField(max_length=255, verbose_name="Subject")
    body_html = tinymce_models.HTMLField()
    body = models.TextField(null=True, blank=True)

    used_for = models.CharField(
        max_length=200,
        choices=USUAGE,
        default='',
        null=True
    )
    active = models.BooleanField(default=True, verbose_name="Is Active")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Template"
        verbose_name_plural = "Templates"
