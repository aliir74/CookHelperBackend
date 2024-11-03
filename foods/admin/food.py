from django.contrib import admin
from foods.models import Food


class FoodAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_per_page = 10


admin.site.register(Food, FoodAdmin)
