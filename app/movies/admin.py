from django.contrib import admin

from .models import MoviesModel, MovieVideoModel

class MovieVodeoInline(admin.TabularInline):
    model = MovieVideoModel
    extra = 2



class MoviesModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'is_featured', 'created_on', 'updated_on')
    list_filter = ('is_active', 'is_featured', 'created_on', 'updated_on')
    search_fields = ('title', 'description', 'short_description')
    # prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20

    readonly_fields = ["created_on","updated_on",]
    filter_horizontal = ['actors', 'directors', 'genres']

    edit_list_display = ('is_active', 'is_featured',)

    inlines = [MovieVodeoInline]


# class MovieVideoModelAdmin(admin.ModelAdmin):
#     list_display = ('movie', 'is_trailer', 'created_on', 'updated_on')
#     list_filter = ('is_trailer', 'created_on', 'updated_on')
#     search_fields = ('movie__title',)
#     raw_id_fields = ('movie',)


admin.site.register(MoviesModel, MoviesModelAdmin)
# admin.site.register(MovieVideoModel, MovieVideoModelAdmin)