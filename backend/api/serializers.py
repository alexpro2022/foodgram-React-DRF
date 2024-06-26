from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from users.models import User

from .fields import Base64ImageField
from .utils import fail


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UserGetSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and user.followers.filter(author_subscription=obj).exists())

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed')


class UserSubscribeSerializer(UserGetSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_recipes(self, author):
        recipes = author.recipes.all()
        limit = self.context.get('request').query_params.get('recipes_limit')
        try:
            recipes = recipes[:int(limit)]
        except (TypeError, ValueError):
            pass
        fields = ('id', 'name', 'image', 'cooking_time')
        return RecipeSerializer(recipes, many=True, fields=fields).data

    def get_recipes_count(self, author):
        return author.recipes.count()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class CustomTagsField(serializers.Field):
    def to_representation(self, value):
        return TagSerializer(value, many=True).data

    def to_internal_value(self, data):
        for item in data:
            if not Tag.objects.filter(pk=item).exists():
                fail(f'Тега с id={item} не существует')
        return data


class RecipeSerializer(DynamicFieldsModelSerializer):
    tags = CustomTagsField()
    author = UserGetSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault())
    ingredients = RecipeIngredientSerializer(
        many=True, source='recipeingredient_set')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        exclude = ('created',)
        validators = [
            UniqueTogetherValidator(
                queryset=Recipe.objects.all(),
                fields=['author', 'name'])]

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and user.favorites.filter(recipe=obj).exists())

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and user.shopping_cart.filter(recipe=obj).exists())

    def _create_or_update(self, validated_data, instance):
        if instance is None:
            return (Recipe.objects.create(**validated_data), True)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return (instance, False)

    def _perform(self, validated_data, inst=None):
        ingredients = validated_data.pop('recipeingredient_set')
        tags = validated_data.pop('tags')
        recipe, created = self._create_or_update(validated_data, inst)
        recipe.tags.set(tags)
        if not created:
            recipe.ingredients.clear()
        recipe_ingredients = []
        for item in ingredients:
            id = item['ingredient']['id']
            ingredient = Ingredient.objects.filter(pk=id)
            if not ingredient.exists():
                fail(f'Ингредиента с id={id} не существует')
            recipe_ingredients.append(RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient[0],
                amount=item['amount'],
            ))
        RecipeIngredient.objects.bulk_create(recipe_ingredients)
        '''
        ===The below code is less efficient DB hits wise===
        for ingredient in ingredients:
            id = ingredient['ingredient']['id']
            if not Ingredient.objects.filter(pk=id).exists():
                fail(f'Ингредиента с id={id} не существует')
            recipe.ingredients.add(
                id,
                through_defaults={'amount': ingredient['amount']})'''
        return recipe

    def create(self, validated_data):
        return self._perform(validated_data)

    def update(self, instance, validated_data):
        return self._perform(validated_data, instance)
