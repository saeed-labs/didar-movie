from django.contrib import admin

from .models import ActorsModel, DirectorModel, GenreModel


class ActorsModelAdmin(admin.ModelAdmin):

    list_display = ('name', 'slug', 'created_on', 'updated_on')
    list_filter = ('created_on', 'updated_on')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class DirectorModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_on', 'updated_on')
    list_filter = ('created_on', 'updated_on')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class GenreModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug', 'created_on', 'updated_on')
    list_filter = ('parent', 'created_on', 'updated_on')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}



admin.site.register(ActorsModel, ActorsModelAdmin)
admin.site.register(DirectorModel, DirectorModelAdmin)
admin.site.register(GenreModel, GenreModelAdmin)
