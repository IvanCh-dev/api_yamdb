from django.contrib import admin

from apiart.models import (Category, Comment,
                           Genre, Review,
                           Title, TitleGenre)
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
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(TitleGenre)
