from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(unique=True, verbose_name='Название категории')
    slug = models.SlugField(unique=True, verbose_name='URL')

    class Meta:
        db_table = "tag"
        verbose_name="Категория"
        verbose_name_plural="Категории"
        ordering = ("name",)

class Ingredient(models.Model):
    name = models.CharField(unique=True, verbose_name='Название ингредиента')
    unit = models.CharField(verbose_name='Единица изменения')

    class Meta:
        db_table = "ingredient"
        verbose_name="Ингридиент"
        verbose_name_plural="Ингридиенты"
        ordering = ("name",)

class Recipe(models.Model):
    name = models.CharField(unique=True, verbose_name='Заголовок рецепта')
    description = models.TextField(verbose_name='Текстовое описание')
    image = models.ImageField(upload_to='recipe_images', verbose_name='Изображение')
    tag = models.ForeignKey(to=Tag, on_delete=models.SET_NULL, verbose_name='Категория')
    ingredient = models.ManyToManyField(to=Ingredient, through="RecipeIngredientAmount", verbose_name='Ингридиент')
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        db_table = "recipe"
        verbose_name="Рецепт"
        verbose_name_plural="Рецепты"
        ordering = ("name",)

class RecipeIngredientAmount(models.Model):
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(to=Ingredient, on_delete=models.CASCADE)
    amount = models.SmallIntegerField(verbose_name="количество")