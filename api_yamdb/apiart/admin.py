from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre


class GenreInline(admin.TabularInline):
    model = Title.genre.through


class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name__startswith", )
    empty_value_display = ('-пусто-')

    class Meta:
        ordering = ("name", "slug")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name__startswith", )
    empty_value_display = ('-пусто-')

    class Meta:
        ordering = ("name", "slug")


class TitleAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "category", "year")
    search_fields = ("name__startswith", "gerne", "category", "year")
    empty_value_display = ('-пусто-')
    exclude = ("genre", )
    inlines = (
        GenreInline,
    )

    class Meta:
        ordering = ("name", "genre", "category")


class TtileGenreAdmin(admin.ModelAdmin):
    list_display = ("title", "genre")
    search_fields = ("title__startswith", "genre__startswith",)
    empty_value_display = ('-пусто-')

    class Meta:
        ordering = ("title", "genre")


admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(TitleGenre, TtileGenreAdmin)
admin.site.register(Review)
admin.site.register(Comment)
