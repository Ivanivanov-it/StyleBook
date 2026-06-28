from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    max_syles = models.PositiveIntegerField(default=40)

    # @property
    # def created_styes(self):
    #     return self.styles.coount()
    #
    # @property
    # def can_create_style(self):
    #     return self.created_styles < self.max_syles