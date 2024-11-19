from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


from foodgram.constants import (
    COOKING_TIME_MIN,
    ERROR_MESSAGE,
    INGREDIENT_AMOUNT_MIN,
    INGREDIENT_LENGTH_LIMIT,
    RECIPE_LENGTH_LIMIT,
    TAG_LENGTH_LIMIT,
    UNIT_LENGTH_LIMIT,
)

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=TAG_LENGTH_LIMIT, unique=True, verbose_name="Название категории"
    )
    slug = models.SlugField(
        max_length=TAG_LENGTH_LIMIT,
        unique=True,
        verbose_name="URL",
    )

    class Meta:
        db_table = "tag"
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=INGREDIENT_LENGTH_LIMIT,
        unique=True,
        verbose_name="Название ингредиента",
    )
    measurement_unit = models.CharField(
        max_length=UNIT_LENGTH_LIMIT, verbose_name="Единица изменения"
    )

    class Meta:
        db_table = "ingredient"
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"
        ordering = ("name",)
        constraints = (
            models.UniqueConstraint(
                fields=("name", "measurement_unit"),
                name="unique_ingredient",
            ),
        )

    def __str__(self) -> str:
        return f"{self.name}, {self.measurement_unit}"


class Recipe(models.Model):
    name = models.CharField(
        max_length=RECIPE_LENGTH_LIMIT, unique=True, verbose_name="Заголовок рецепта"
    )
    text = models.TextField(verbose_name="Текстовое описание")
    tags = models.ManyToManyField(to=Tag, verbose_name="Категория")
    ingredients = models.ManyToManyField(
        to=Ingredient, through="recipes.RecipeIngredient", verbose_name="Ингридиент"
    )
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Автор")
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(COOKING_TIME_MIN, ERROR_MESSAGE.get("time_error")),
        ),
        verbose_name="Время приготовления",
    )
    image = models.ImageField(
        upload_to="media/recipe_images/", verbose_name="Изображение"
    )
    is_published = models.BooleanField(default=True, verbose_name="Отображение")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    class Meta:
        db_table = "recipe"
        default_related_name = "recipes"
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class RecipeTags(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="tag_list", verbose_name="Recipe"
    )
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE, related_name="tag_recipe", verbose_name="Tag"
    )


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(to=Ingredient, on_delete=models.PROTECT)
    amount = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(INGREDIENT_AMOUNT_MIN, ERROR_MESSAGE.get("amount_error")),
        ),
        verbose_name="количество",
    )


class Favorite(models.Model):
    user = models.ForeignKey(to=User, related_name="favorite", on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        to=Recipe, related_name="favorite", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["-id"]
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"

        constraints = (
            models.UniqueConstraint(
                fields=("user", "recipe"), name="unique_favorite_recipe"
            ),
        )


class ShoppingList(models.Model):
    user = models.ForeignKey(
        to=User, related_name="shopping_list", on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        to=Recipe, related_name="shopping_list", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Списоки покупок"

        constraints = (
            models.UniqueConstraint(
                fields=("user", "recipe"), name="unique_shopping_list_recipe"
            ),
        )
