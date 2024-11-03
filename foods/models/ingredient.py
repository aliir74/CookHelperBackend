import enum

from django.db import models
from django.utils.translation import gettext_lazy as _


class IngredientTypeOrder(enum.Enum):
    MEAT = 0
    EGG = 1
    GRAIN = 2
    VEGETABLE = 3
    FRUIT = 4
    DIARY = 5
    BREAD = 6
    OTHER = 7


class Ingredient(models.Model):
    class IngredientType(models.TextChoices):
        VEGETABLE = "VEGETABLE", _("Vegetable")
        FRUIT = "FRUIT", _("Fruit")
        MEAT = "MEAT", _("Meat")
        BREAD = "BREAD", _("Bread")
        DIARY = "DIARY", _("Diary")
        EGG = "EGG", _("Egg")
        GRAIN = "GRAIN", _("Grain")
        OTHER = "OTHER", _("Other")

    name = models.TextField()
    type = models.TextField(
        default=IngredientType.OTHER, choices=IngredientType.choices
    )
