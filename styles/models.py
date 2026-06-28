from django.conf import settings
from django.db import models

from common.models import GameClass, CreatedAtMixin


# Create your models here.


class Style(CreatedAtMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)

    game_class = models.CharField(max_length=25,choices=GameClass.choices,default=GameClass.WARRIOR_MALE)

    thumbnail = models.ImageField(upload_to="thumbnails/")
    can_be_saved = models.BooleanField(default=False)
    requires_custom_file = models.BooleanField(default=False)

    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_by", blank=True)
    downloads = models.PositiveIntegerField(default=0)

class StyleImage(models.Model):
    style = models.ForeignKey(Style, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="styles/")

class StyleFile(models.Model):
    style = models.ForeignKey(Style, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="customizations/")

class Favourite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    style = models.ForeignKey(Style, on_delete=models.CASCADE)



