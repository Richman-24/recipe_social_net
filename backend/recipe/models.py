from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

NAME_MAX_LENGTH = 64

class Tag(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=NAME_MAX_LENGTH, unique=True, verbose_name='URL')

    class Meta:
        db_table = "tag"
        verbose_name="Категория"
        verbose_name_plural="Категории"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True, verbose_name='Название ингредиента')
    unit = models.CharField(max_length=NAME_MAX_LENGTH, verbose_name='Единица изменения')

    class Meta:
        db_table = "ingredient"
        verbose_name="Ингридиент"
        verbose_name_plural="Ингридиенты"
        ordering = ("name",)

    def __str__(self) -> str:
        return f"{self.name}, {self.unit}"

class Recipe(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True, verbose_name='Заголовок рецепта')
    description = models.TextField(verbose_name='Текстовое описание')
    image = models.ImageField(upload_to='recipe_images', verbose_name='Изображение')
    tag = models.ManyToManyField(to=Tag, verbose_name='Категория')
    ingredient = models.ManyToManyField(to=Ingredient, through="recipe.RecipeIngredientAmount", verbose_name='Ингридиент')
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Автор')
    cooking_time = models.SmallIntegerField(verbose_name='Время приготовления')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    is_active = models.BooleanField(default=True, verbose_name='Отображение')

    class Meta:
        db_table = "recipe"
        default_related_name='recipe'
        verbose_name="Рецепт"
        verbose_name_plural="Рецепты"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name
    
class RecipeIngredientAmount(models.Model):
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(to=Ingredient, on_delete=models.CASCADE)
    amount = models.SmallIntegerField(verbose_name="количество")