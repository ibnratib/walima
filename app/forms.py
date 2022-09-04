
import email
from django import forms
from app.models import *
from django.forms import inlineformset_factory
from django.db.models import Q
from zxcvbn_password import zxcvbn
from zxcvbn_password.fields import PasswordField, PasswordConfirmationField

# Importations application
import app.m00_common as m00
import app.models as am


class RegistreForm(forms.Form):
    user_name = forms.CharField(max_length=200)
    email = forms.EmailField(max_length=200)
    telephone = forms.CharField(max_length=40)
    ville = forms.ChoiceField(choices=m00.VILLES_MAROC)
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


class ServicePartenaireForm(forms.Form):
    service = forms.ModelChoiceField(queryset=am.Service.objects.all())
    description_de_service = forms.CharField(widget=forms.Textarea(attrs={}))
    images_de_service = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    

    def __init__(self, *args, **kwargs):
        super(ServicePartenaireForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
