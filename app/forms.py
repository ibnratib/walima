
import email
from django import forms
from app.models import *
from django.forms import inlineformset_factory
from django.db.models import Q
from zxcvbn_password import zxcvbn
from zxcvbn_password.fields import PasswordField, PasswordConfirmationField


VILLE_CHOICES = (
    ('', 'Choisir ville'), ('Tanger', 'Tanger'),
    ('Agadir', 'Agadir'), ('Béni Mellal', 'Béni Mellal'),
    ('Chefchaouen', 'Chefchaouen'), ('El Jadida', 'El Jadida'),
    ('Fés', 'Fés'), ('Kénitra', 'Kénitra'),
    ('Khémisset', 'Khémisset'), ('Khouribga', 'Khouribga'),
    ('Marrakech', 'Marrakech'), ('Meknès', 'Meknès'),
    ('Mohammédia', 'Mohammédia'), ('Nador', 'Nador'),
    ('Oujda', 'Oujda'), ('Rabat', 'Rabat'),
    ('Safi', 'Safi'), ('Salé', 'Salé'), ('Taza', 'Taza'),
    ('Témara', 'Témara'), ('Tétouan', 'Tétouan'),
    ('Khémisset', 'Khémisset'),)

class RegistreForm(forms.Form):
    user_name = forms.CharField(max_length=200)
    email = forms.EmailField(max_length=200)
    telephone = forms.CharField(max_length=40)
    ville = forms.ChoiceField(choices=VILLE_CHOICES)
    password = forms.PasswordInput()
    password_repeat = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    def __init__(self, *args, **kwargs):
        super(RegistreForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['user_name'].widget.attrs['placeholder'] = 'Nom utilisateur'
        self.fields['ville'].widget.attrs['placeholder'] = 'Choisir la ville'
        self.fields['email'].widget.attrs['placeholder'] = 'Saisir votre email professionnel'
        self.fields['telephone'].widget.attrs['placeholder'] = 'Saisir votre numero de telephone professionnel'


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Saisir votre email professionnel'

