from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Food, Ingredient
from .models.ingredient import IngredientTypeOrder
from .serializers import FoodSerializer, IngredientSerializer


class LandingPageView(APIView):
    type_order = {
        _("Meat"): IngredientTypeOrder.MEAT.value,
        _("Egg"): IngredientTypeOrder.EGG.value,
        _("Grain"): IngredientTypeOrder.GRAIN.value,
        _("Vegetable"): IngredientTypeOrder.VEGETABLE.value,
        _("Fruit"): IngredientTypeOrder.FRUIT.value,
        _("Diary"): IngredientTypeOrder.DIARY.value,
        _("Bread"): IngredientTypeOrder.BREAD.value,
        _("Other"): IngredientTypeOrder.OTHER.value,
    }

    type_icons = {
        _("Meat"): "🥩",
        _("Egg"): "🥚",
        _("Grain"): "🌾",
        _("Vegetable"): "🥬",
        _("Fruit"): "🍎",
        _("Diary"): "🥛",
        _("Bread"): "🍞",
        _("Other"): "❓",
    }

    def get_ingredients_by_type(self):
        ingredients_by_type = {}
        for ingredient in Ingredient.objects.all().order_by("name"):
            type_display = _(ingredient.get_type_display())
            if type_display not in ingredients_by_type:
                ingredients_by_type[type_display] = {
                    "icon": self.type_icons[type_display],
                    "ingredients": [],
                }
            ingredients_by_type[type_display]["ingredients"].append(
                IngredientSerializer(ingredient).data
            )

        return {
            k: v
            for k, v in sorted(
                ingredients_by_type.items(), key=lambda x: self.type_order[x[0]]
            )
        }

    def get(self, request):
        return Response(
            {
                "ingredients_by_type": self.get_ingredients_by_type(),
                "foods": [],
                "selected_ingredients": [],
            }
        )

    def post(self, request):
        selected_ingredients = request.data.get("ingredients", [])
        sort_by = request.data.get("sort_by", "difficulty")

        selected_ingredients_names = [
            ingredient["name"] for ingredient in selected_ingredients
        ]
        # Get foods containing selected ingredients
        foods = Food.objects.filter(
            ingredients__name__in=selected_ingredients_names
        ).distinct()
        # Process foods with matched/missing ingredients
        processed_foods = []
        for food in foods:
            matched = len(
                set(
                    food.ingredients.filter(
                        name__in=selected_ingredients_names
                    ).values_list("name", flat=True)
                )
            )
            missing = len(food.ingredients.all()) - matched

            if missing <= 2:  # Keep max 2 missing ingredients rule
                processed_foods.append(
                    {"food": food, "matched": matched, "missing": missing}
                )
        # Sort foods by missing ingredients and user preference
        foods_by_missing = {0: [], 1: [], 2: []}
        for item in processed_foods:
            foods_by_missing[item["missing"]].append(item)
        # Sort each group
        for missing_count in foods_by_missing:
            if sort_by == "cooking_time":
                foods_by_missing[missing_count].sort(
                    key=lambda x: x["food"].cooking_time
                )
            elif sort_by == "difficulty":
                difficulty_order = {
                    _("Easy"): 0,
                    _("Medium"): 1,
                    _("Hard"): 2,
                }
                foods_by_missing[missing_count].sort(
                    key=lambda x: difficulty_order[
                        _(x["food"].get_difficulty_display())
                    ]
                )
            else:  # sort by name
                foods_by_missing[missing_count].sort(key=lambda x: x["food"].name)
        # Combine sorted groups
        final_foods = []
        for missing_count in sorted(foods_by_missing.keys()):
            for item in foods_by_missing[missing_count]:
                food_data = FoodSerializer(item["food"]).data
                food_data["matched_ingredients"] = item["matched"]
                food_data["missing_ingredients"] = item["missing"]
                final_foods.append(food_data)

        return Response(
            {
                "ingredients_by_type": self.get_ingredients_by_type(),
                "foods": final_foods,
                "selected_ingredients": selected_ingredients,
            }
        )
