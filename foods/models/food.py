from django.db import models
from django.utils.translation import gettext_lazy as _

from .ingredient import Ingredient


class Food(models.Model):
    class Difficulty(models.TextChoices):
        EASY = "EASY", _("Easy")
        MEDIUM = "MEDIUM", _("Medium")
        HARD = "HARD", _("Hard")

    name = models.TextField()
    start_to_work_time = models.IntegerField(default=0)
    working_time = models.IntegerField()
    cooking_time = models.IntegerField()
    ingredients = models.ManyToManyField(Ingredient, related_name="foods")
    instructions = models.TextField(default="")
    difficulty = models.TextField(choices=Difficulty.choices)
