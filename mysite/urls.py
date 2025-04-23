"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from myproject import views
# Importe für die Umlenkung der Mediendateien
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # localhost:8000
    path('', views.start_view, name='start'), # Pfad für die Startseite
    # Benutzeranmeldung bereitstellen
    path('benutzer/', include('django.contrib.auth.urls')),
    path("register/", views.register, name="register"),
    path('anmelden/', views.logout_view, name='logout_view'), # Abmelden
    path('home/', views.home, name='home'), # Pfad für die Homeseite
    path('film/<int:film_id>/', views.film_details, name='film_details'), # Pfad um auf die Detailseite zu kommen
    path('film/<int:film_id>/kommentar/', views.kommentar_erstellen, name='kommentar_erstellen'), # Pfad um auf die KOmmentar seite zu kommen
    path('search/', views.search, name='search'),
    path('film/<int:film_id>/favorisieren/', views.favorisieren, name='favorisieren'),
    path('favoriten/', views.favoriten_liste, name='favoriten_liste'), # Pfad für die Suchfunktion
    path('kinokarte/', views.kinokarte, name='kinokarte'),  # Neue Route für die Kinokarte
    path('kalender/<int:year>/<int:month>/', views.kalender_view, name='kalender'), 
    path('movies/', views.movie, name='movie'), # Pfad für die Homeseite
    path('movie/<int:movie_id>/', views.movie_details, name='movie_details'),
    path('search2/', views.search2, name='search2'),
    path('profil/', views.profil_view, name='profil'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # ergänzt die Pfade zum Medienordner, wenn der Server veröffentlicht wird
