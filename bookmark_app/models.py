from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Platform(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Bookmark(models.Model):
    url = models.URLField()
    title = models.TextField()
    platform_name = models.ForeignKey(Platform, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.platform_name}: {self.title}"
