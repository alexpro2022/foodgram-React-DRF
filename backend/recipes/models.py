from django.core.validators import MinValueValidator
from django.db import models

from users.models import User

from .validators import validate_color, validate_slug


class Tag(models.Model):
    name = models.CharField('Название', max_length=200)
    color = models.CharField(
        'Цветовой HEX-код', max_length=7, validators=[validate_color],
        help_text='Цветовой HEX-код (например: #49B64E)')
    slug = models.SlugField(
        'Уникальный слаг', max_length=200,
        unique=True, validators=[validate_slug])

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=200, db_index=True)
    measurement_unit = models.CharField('Единица измерения', max_length=200)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='ingredient_unique_unit')]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes', verbose_name='Автор рецепта')
    name = models.CharField('Название', max_length=200, db_index=True)
    text = models.TextField('Описание')
    created = models.DateField('Дата публикации', auto_now_add=True)
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/images/',
        null=True,
        default=None)
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient',
        verbose_name='Ингредиенты', help_text='Ингредиенты')
    tags = models.ManyToManyField(
        Tag, verbose_name='Теги',
        help_text='Можно установить несколько тегов на один рецепт')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления (в минутах)',
        validators=[MinValueValidator(1, 'Минимальное значение = 1')],
        help_text='Время приготовления (в минутах)')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'name'], name='author_unique_recipe')]

    def __str__(self):
        return f'Рецепт: {self.name} от {self.author}'

# Below methods are for the admin-zone
    def get_ingredients(self):
        ingredients = set()
        for item in self.ingredients.all():
            amount = str(
                RecipeIngredient.objects.get(
                    recipe=self, ingredient=item).amount)
            ingredients.add(
                ' '.join((item.name, '-', amount, item.measurement_unit, '\n'))
            )
        return sorted(ingredients)

    def get_tags(self):
        tags_names = set()
        for item in self.tags.all():
            tags_names.add(item.name)
        return ', '.join(sorted(tags_names))

    def get_favorites_count(self):
        return self.is_favorited.count()


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингридиент')
    amount = models.PositiveSmallIntegerField(
        'Количество', help_text='Минимальное значение: 1',
        validators=[MinValueValidator(1, 'Минимальное значение: 1')])

    class Meta:
        verbose_name = 'Ингредиенты для рецептов'
        verbose_name_lural = 'Ингредиенты для рецептов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient', 'amount'],
                name='unique_recipe_ingredient_amount')]


class Favorites(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorites', verbose_name='Потребитель')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='is_favorited', verbose_name='Рецепт')
    added = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        ordering = ('-added',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favourite')]

    def __str__(self):
        return f'Рецепт {self.recipe} в списке избранного {self.user}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='shopping_cart', verbose_name='Потребитель')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='is_in_shopping_cart', verbose_name='Рецепт')
    added = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        ordering = ('-added',)
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_cart')]

    def __str__(self):
        return f'Рецепт {self.recipe} в списке покупок {self.user}'
