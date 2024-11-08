# Generated by Django 5.1.2 on 2024-10-29 14:18

import json
import logging
from typing import TYPE_CHECKING

from django.db import migrations

if TYPE_CHECKING:
    from foods.models.food import Food
    from foods.models.ingredient import Ingredient

logger = logging.getLogger(__name__)


def seed_database(apps, schema_editor):
    Ingredient: "Ingredient" = apps.get_model("foods", "Ingredient")
    Food: "Food" = apps.get_model("foods", "Food")
    with open("foods/fixtures/ingredients.json", "r") as file:
        ingredients = json.load(file)
        for ingredient in ingredients:
            Ingredient.objects.update_or_create(**ingredient)
    with open("foods/fixtures/foods.json", "r") as file:
        foods = json.load(file)
        for food in foods:
            ingredients = food.pop("ingredients")
            food_obj = Food.objects.create(**food)
            for ingredient in ingredients:
                try:
                    ingredient_obj = Ingredient.objects.get(name=ingredient)
                except Ingredient.DoesNotExist:
                    logger.error(f"Ingredient {ingredient} does not exist")
                food_obj.ingredients.add(ingredient_obj)


class Migration(migrations.Migration):

    dependencies = [
        ("foods", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_database, migrations.RunPython.noop),
    ]
