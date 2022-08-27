
# Importations Django
from django.db import models
from django.contrib.auth.models import User

# Importations Application
import app.m00_common as m00

# Create your models here.

class ClientProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='client_profile')
    ville = models.CharField(
        max_length=100,
        blank=False,
        null=False)
    telephone_mobile = models.CharField(
        max_length=50,
        blank=False,
        null=False)
    type_client = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        choices=m00.CLIENT_TYPES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


class Service(models.Model):
    nom_service = models.CharField(
        max_length=200,
        blank=False,
        null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom_service


class ServicePartenaire(models.Model):
    client_profile = models.ForeignKey(
        ClientProfile,
        on_delete=models.CASCADE,
        null=False,
        blank=False)
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        null=False,
        blank=False)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.service.nom_service


class ImageServicePartenaire(models.Model):
    service_partenaire = models.ForeignKey(
        ServicePartenaire,
        on_delete=models.CASCADE,
        null=False,
        blank=False)
    image = models.ImageField(upload_to ='uploads/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class EvenementClient(models.Model):
    client_profile = models.ForeignKey(
        ClientProfile,
        on_delete=models.CASCADE,
        null=False,
        blank=False)
    type_evenement = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        choices=m00.EVENEMENT_TYPES)
    nombre_invites = models.PositiveIntegerField(null=False, blank=False, default=1)
    date = models.DateTimeField(blank=False, null=False)

    ville = models.CharField(
        max_length=200,
        blank=False,
        null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type_evenement
    

class ServiceEvenement(models.Model):
    evenement_client = models.ForeignKey(
        EvenementClient,
        on_delete=models.CASCADE,
        null=False,
        blank=False)
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        null=False,
        blank=False)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class MessageService(models.Model):
    service_evenement = models.ForeignKey(
        ServiceEvenement,
        on_delete=models.CASCADE,
        null=False,
        blank=False)
    profil_client = models.ForeignKey(
        ClientProfile,
        on_delete=models.CASCADE,
        null=False,
        blank=False)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
