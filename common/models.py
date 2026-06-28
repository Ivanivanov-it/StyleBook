from django.db import models

# Create your models here.


class CreatedAtMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class GameClass(models.TextChoices):
    WARRIOR_MALE = "Warrior(Male)", "Warrior(Male)"
    WARRIOR_FEMALE = "Warrior(Female)", "Warrior(Female)"
    MAGE = "Mage", "Mage"
    MARTIAL_ARTIST_FEMALE = "Martial Artist(Female)", "Martial Artist(Female)"
    MARTIAL_ARTIST_MALE = "Martial Artist(Male)", "Martial Artist(Male)"
    GUNNER_MALE = "Gunner(Male)", "Gunner(Male)"
    GUNNER_FEMALE = "Gunner(Female)", "Gunner(Female)"
    ASSASSIN = "Assassin", "Assassin"
    SPECIALIST = "Specialist", "Specialist"
    GUARDIANKNIGHT = "Guardianknight", "Guardianknight"
