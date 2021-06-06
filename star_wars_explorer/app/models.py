from django.db import models
from django.urls import reverse


# Create your models here.


class Collection(models.Model):
    file_name = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.file_name

    def get_absolute_url(self):
        return reverse("collection_detail", args=[str(self.id)])
