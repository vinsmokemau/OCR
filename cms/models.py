from django.db import models
from django.urls import reverse


class Image(models.Model):

    image = models.ImageField(
        'imagen',
        upload_to='images',
    )
    excel = models.FileField(
        blank=True,
    )

    def get_absolute_url(self):
        return reverse('cms:image-detail', kwargs={'image_id': self.pk})
