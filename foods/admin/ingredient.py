from django.contrib import admin
from foods.models import Ingredient


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_per_page = 10


admin.site.register(Ingredient, IngredientAdmin)
