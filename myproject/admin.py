

from django.contrib import admin
from .models import Film, Kommentar, Favorit, Event, Movie, UserProfile

# Admin für Filme
@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date')  # Zeigt Titel & Kinostart
    search_fields = ('title',)  # Suchfeld für Titel
    list_filter = ('release_date',)  # Filter für Kinostart

# Admin für Kommentare
@admin.register(Kommentar)
class KommentarAdmin(admin.ModelAdmin):
    list_display = ('user', 'film', 'created_at')  # 'autor' zu 'user', 'datum' zu 'created_at'
    search_fields = ('user__username', 'film__title')  # 'autor' zu 'user__username'
    list_filter = ('created_at',)  # 'datum' zu 'created_at'

# Admin für Favoriten
@admin.register(Favorit)
class FavoritAdmin(admin.ModelAdmin):
    list_display = ('user', 'film', 'hinzugefügt_am')
    search_fields = ('user__username', 'film__title')
    list_filter = ('hinzugefügt_am',)

# Admin für Events
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    search_fields = ('title',)
    list_filter = ('date',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('image',)