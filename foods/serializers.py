from rest_framework import serializers


class IngredientSerializer(serializers.Serializer):
    name = serializers.CharField()
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        return obj.get_type_display()


class FoodSerializer(serializers.Serializer):
    name = serializers.CharField()
    start_to_work_time = serializers.IntegerField()
    working_time = serializers.IntegerField()
    cooking_time = serializers.IntegerField()
    ingredients = IngredientSerializer(many=True)
    instructions = serializers.CharField()
    difficulty = serializers.SerializerMethodField()

    def get_difficulty(self, obj):
        return obj.get_difficulty_display()
