from django.contrib import admin

from recipes.models import Recipe, RecipeIngredient, Tag, Ingredient

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1 
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("name",)}
    list_display = ["name",]

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ["name", "measurement_unit"]

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ["name", "author", 'pub_date', 'is_published']
    search_fields = ('name',)