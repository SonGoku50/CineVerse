from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Film(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='static/images/')
    release_date = models.DateField(null=True, blank=True)
    trailer_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

class Kommentar(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='kommentare')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Optional gemacht
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username if self.user else "Anonym"} - {self.film.title}'

class Favorit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="favoriten")
    hinzugefügt_am = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} liebt {self.film.title}'

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField(default="Keine Beschreibung verfügbar")
    image = models.ImageField(upload_to='static/images/', null=True, blank=True, default='static/images/default_event.jpg')

    def __str__(self):
        return self.title

class Movie(models.Model):
    title = models.CharField(max_length=100)
    link = models.URLField(default="Kein Film verfügbar")
    image = models.ImageField(upload_to='static/images/', default='images/default.jpg')
    release_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/profile_images/', default='profile_images/default.jpg')
    bio = models.TextField(blank=True)
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)

    def add_xp(self, xp_amount):
        """Fügt XP hinzu und prüft auf Level-Up."""
        self.xp += xp_amount
        required_xp = self.level * 100
        while self.xp >= required_xp:
            self.level += 1
            required_xp = self.level * 100
        self.save()

    @property
    def xp_percentage(self):
        """Berechnet den Fortschritt zum nächsten Level in Prozent."""
        current_level_xp = (self.level - 1) * 100
        next_level_xp = self.level * 100
        progress = self.xp - current_level_xp
        total = next_level_xp - current_level_xp
        return (progress / total) * 100 if total > 0 else 0

    def __str__(self):
        return f"{self.user.username}'s Profil"

# Signale für automatische Profil-Erstellung
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

