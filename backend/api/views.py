from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import (Favorites, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.models import Subscribe, User

from .filters import RecipesFilter
from .pagination import CustomPageLimitPaginator
from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeSerializer,
                          TagSerializer, UserSubscribeSerializer)
from .utils import delete_object_or_400, fail


class UserViewSet(DjoserViewSet):
    http_method_names = ('get', 'post', 'delete', 'head', 'options')
    pagination_class = CustomPageLimitPaginator

    @action(('POST', 'DELETE'), detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, pk=id)
        user = request.user
        if user == author:
            fail('Самоподписка не возможна!!!')

        if request.method == 'DELETE':
            delete_object_or_400(
                Subscribe, subscribed_user=user, author_subscription=author)
            return Response(status=status.HTTP_204_NO_CONTENT)

        _, created = Subscribe.objects.get_or_create(
            subscribed_user=user,
            author_subscription=author)
        if not created:
            fail(
                f'Подписка {user.username} '
                f'на {author.username} уже существует')
        return Response(
            data=UserSubscribeSerializer(
                author, context={'request': request}
            ).data,
            status=status.HTTP_201_CREATED)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        authors = User.objects.filter(authors__subscribed_user=user)
        page = self.paginate_queryset(authors)
        if page is None:
            return Response(
                data=UserSubscribeSerializer(
                    authors, context={'request': request}, many=True
                ).data,
                status=status.HTTP_200_OK)
        return self.get_paginated_response(
            data=UserSubscribeSerializer(
                page, context={'request': request}, many=True
            ).data)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (SearchFilter, )
    search_fields = ('^name',)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipesFilter
    pagination_class = CustomPageLimitPaginator
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def _param(self, param_name):
        try:
            return int(self.request.query_params.get(param_name)) == 1
        except (TypeError, ValueError):
            return False

    def get_queryset(self):
        recipes = Recipe.objects.all()
        current_user = self.request.user
        if current_user.is_anonymous:
            return recipes
        if self._param('is_favorited'):
            recipes = recipes.filter(is_favorited__user=current_user)
        if self._param('is_in_shopping_cart'):
            recipes = recipes.filter(is_in_shopping_cart__user=current_user)
        return recipes

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def _delete_recipe_from(self, model, user, recipe):
        delete_object_or_400(model, user=user, recipe=recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _add_recipe_to(self, model, user, recipe):
        _, created = model.objects.get_or_create(
            user=user, recipe=recipe)
        if not created:
            fail(f'Рецепт уже существует в {model.__name__}')
        return Response(
            RecipeSerializer(
                recipe,
                fields=('id', 'name', 'image', 'cooking_time')
            ).data,
            status.HTTP_201_CREATED)

    def _perform(self, model, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'DELETE':
            return self._delete_recipe_from(model, user=user, recipe=recipe)
        return self._add_recipe_to(model, user=user, recipe=recipe)

    @action(('POST', 'DELETE'), detail=True)
    def favorite(self, request, pk=None):
        return self._perform(Favorites, request, pk)

    @action(('POST', 'DELETE'), detail=True)
    def shopping_cart(self, request, pk=None):
        return self._perform(ShoppingCart, request, pk)

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        user = request.user
        recipes = Recipe.objects.filter(is_in_shopping_cart__user=user)
        ingredients = RecipeIngredient.objects.filter(
            recipe__in=recipes).order_by('ingredient__name').values_list(
                'ingredient__name',
                'amount',
                'ingredient__measurement_unit')
        amounts = {}
        for ingredient, amount, unit in ingredients:
            key = f'{ingredient}, {unit}:'
            amounts[key] = amount + amounts.get(key, 0)
        cart = ''
        for key in amounts:
            cart += (
                f'{key} - {amounts[key]}\n')
        return HttpResponse(cart, content_type='text/plain')
