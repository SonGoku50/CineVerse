from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from .models import Film, Kommentar, Favorit, Event, Movie, UserProfile
from .forms import KommentarForm, UserProfileForm, RegisterForm

import calendar
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login


# Create your views here.
def start_view(request):
    # Die Startseite aufrufen
    return render(request, 'myproject/start.html')

def logout_view(request):
    # Benutzer ausloggen
    logout(request)
    # Zur Startseite zurückkehren
    return render(request, 'myproject/start.html')

def home(request):
    filme = Film.objects.all().order_by('release_date')  # Sortiert nach Veröffentlichungsdatum
    return render(request, 'myproject/home.html', {'filme': filme})

def film_details(request, film_id):
    film = get_object_or_404(Film, pk=film_id)
    return render(request, 'myproject/film_details.html', {'film': film})

@login_required
def kommentar_erstellen(request, film_id):
    film = get_object_or_404(Film, pk=film_id)
    if request.method == 'POST':
        form = KommentarForm(request.POST)
        if form.is_valid():
            kommentar = form.save(commit=False)
            kommentar.user = request.user
            kommentar.film = film
            kommentar.save()
            # XP vergeben
            request.user.userprofile.add_xp(20)  # Änderung: profile zu userprofile
            messages.success(request, "Kommentar hinzugefügt! +20 XP")
            if request.user.userprofile.xp >= request.user.userprofile.level * 100:  # Änderung: profile zu userprofile
                messages.success(request, f"Glückwunsch! Du hast Level {request.user.userprofile.level} erreicht!")
    return redirect('film_details', film_id=film.id)

def search(request):
    query = request.GET.get('q')
    if query:
        filme = Film.objects.filter(title__icontains=query)
    else:
        filme = Film.objects.none()
    return render(request, 'myproject/search_results.html', {'filme': filme, 'query': query})

@login_required
def favorisieren(request, film_id):
    film = get_object_or_404(Film, pk=film_id)
    if request.method == "POST":
        favorit, erstellt = Favorit.objects.get_or_create(user=request.user, film=film)
        if erstellt:
            # Film wurde zu Favoriten hinzugefügt
            request.user.userprofile.add_xp(10)  # Änderung: profile zu userprofile
            messages.success(request, "Film zu Favoriten hinzugefügt! +10 XP")
        else:
            # Film aus Favoriten entfernen
            favorit.delete()
            request.user.userprofile.add_xp(5)  # Änderung: profile zu userprofile
            messages.success(request, "Film aus Favoriten entfernt! +5 XP")
        # Prüfe auf Level-Up
        if request.user.userprofile.xp >= request.user.userprofile.level * 100:  # Änderung: profile zu userprofile
            messages.success(request, f"Glückwunsch! Du hast Level {request.user.userprofile.level} erreicht!")
    return redirect('film_details', film_id=film.id)

@login_required
def favoriten_liste(request):
    favoriten = Favorit.objects.filter(user=request.user).select_related('film')
    filme = [fav.film for fav in favoriten]
    return render(request, 'myproject/favoriten.html', {'filme': filme})

def kinokarte(request):
    return render(request, 'myproject/kinokarte.html')

def kalender_view(request, year=None, month=None):
    if year is None or month is None:
        today = datetime.today()
        year, month = today.year, today.month
    else:
        year, month = int(year), int(month)

    month_name = calendar.month_name[month]
    month_days = calendar.monthrange(year, month)[1]
    events = Event.objects.filter(date__year=year, date__month=month)

    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    context = {
        "year": year,
        "month": month,
        "month_name": month_name,
        "month_days": range(1, month_days + 1),
        "events": events,
        "prev_month": prev_month,
        "prev_year": prev_year,
        "next_month": next_month,
        "next_year": next_year,
    }
    return render(request, "myproject/kalender.html", context)

def movie(request):
    movies = Movie.objects.all().order_by('title')
    vor_60_tagen = timezone.now().date() - timedelta(days=60)
    neue_filme = Movie.objects.filter(release_date__gte=vor_60_tagen)
    return render(request, 'myproject/movies.html', {'movies': movies, 'neue_filme': neue_filme})

def movie_details(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'myproject/movie_details.html', {'movie': movie})

def search2(request):
    query = request.GET.get('a')
    if query:
        movies = Movie.objects.filter(title__icontains=query)
    else:
        movies = Movie.objects.none()
    return render(request, 'myproject/search_results2.html', {'movies': movies, 'query': query})

@login_required
def profil_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # XP vergeben für Profilaktualisierung
            request.user.userprofile.add_xp(15)  # Änderung: profile zu userprofile
            messages.success(request, "Profil aktualisiert! +15 XP")
            # Prüfe auf Level-Up
            if request.user.userprofile.xp >= request.user.userprofile.level * 100:  # Änderung: profile zu userprofile
                messages.success(request, f"Glückwunsch! Du hast Level {request.user.userprofile.level} erreicht!")
            return redirect('profil')
    else:
        form = UserProfileForm(instance=profile)

    favoriten = Favorit.objects.filter(user=request.user).select_related('film')
    return render(request, 'myproject/profil.html', {
        'form': form,
        'favoriten': favoriten,
        'profile': profile,
        'user': request.user
    })

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})