from django.contrib import admin

from recipe.models import Recipe, RecipeIngredientAmount, Tag, Ingredient

class RecipeIngredientAmountInline(admin.TabularInline):
    model = RecipeIngredientAmount
    extra = 1 
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("name",)}
    list_display = ["name",]

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ["name", "unit"]

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientAmountInline]
    list_display = ["name", "author", 'pub_date', 'is_active']
    search_fields = ('name',)