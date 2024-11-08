# Generated by Django 5.1.2 on 2024-10-29 18:27

from django.db import migrations


def fix_difficulty(apps, schema_editor):
    Food = apps.get_model("foods", "Food")
    for food in Food.objects.all():
        food.difficulty = food.difficulty.capitalize()
        food.save()


class Migration(migrations.Migration):

    dependencies = [
        ("foods", "0002_auto_20241029_1418"),
    ]

    operations = [
        migrations.RunPython(fix_difficulty, migrations.RunPython.noop),
    ]
