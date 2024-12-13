from django.contrib import admin
from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('prompt_1', 'prompt_2', 'created_at')  # Customize displayed fields

