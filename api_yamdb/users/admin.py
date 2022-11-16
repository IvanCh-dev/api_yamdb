from apiart.models import Category, Genre, Title
from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name',
                    'last_name',)
    search_fields = ('username',)
    empty_value_display = '-пусто-'

admin.site.register(User, UserAdmin)

"""зарегала новые модели 2 разраб"""
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Title)