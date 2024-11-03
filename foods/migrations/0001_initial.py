# Generated by Django 5.1.2 on 2024-10-29 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('type', models.TextField(choices=[('VEGETABLE', 'Vegetable'), ('FRUIT', 'Fruit'), ('MEAT', 'Meat'), ('BREAD', 'Bread'), ('DIARY', 'Diary'), ('EGG', 'Egg'), ('GRAIN', 'Grain'), ('OTHER', 'Other')], default='OTHER')),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('start_to_work_time', models.IntegerField(default=0)),
                ('working_time', models.IntegerField()),
                ('cooking_time', models.IntegerField()),
                ('instructions', models.TextField(default='')),
                ('difficulty', models.TextField(choices=[('EASY', 'Easy'), ('MEDIUM', 'Medium'), ('HARD', 'Hard')])),
                ('ingredients', models.ManyToManyField(related_name='foods', to='foods.ingredient')),
            ],
        ),
    ]