from django.db import models


class ExtensionPackage(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=100)
    description = models.TextField()
    zip = models.FileField(upload_to='extensions/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
