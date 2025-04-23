from django import forms
from .models import Film, Kommentar, User, Event, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class KommentarForm(forms.ModelForm):
    class Meta:
        model = Kommentar
        fields = ['content']

class FilmForm(forms.ModelForm):  # Erstellt ein neues Formular für die Filme
   class Meta:
       model = Film
       fields = ['title', 'description', 'image','release_date'] # Felder für die Modelle des Films

class FilmSearchForm(forms.ModelForm): # Erstellt ein neues Formular für die Suchfunktion
   query = forms.CharField(label='Suche', max_length=100, required=True) # Formular für die Suchfunktion

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image', 'bio']
        labels = {
            'image': 'Profilbild',
            'bio': 'Bio',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            'username': 'Benutzername',
            'password1': 'Passwort',
            'password2': 'Passwort bestätigen',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Wähle einen Benutzernamen...',
                'class': 'form-control',
            }),
            'password1': forms.PasswordInput(attrs={
                'placeholder': 'Wähle ein Passwort...',
                'class': 'form-control',
            }),
            'password2': forms.PasswordInput(attrs={
                'placeholder': 'Passwort erneut eingeben...',
                'class': 'form-control',
            }),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError("Der Benutzername muss mindestens 3 Zeichen lang sein.")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Dieser Benutzername ist bereits vergeben.")
        return username

