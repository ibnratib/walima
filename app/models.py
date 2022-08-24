from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# DECLARING GLOBAL VARIABLES

CLIENT_TYPES = [
    ('Client', 'Client'),
    ('Partenaire', 'Partenaire')
]

EVENEMENT_TYPES = [
    ('Marriage', 'Marriage'),
    ('Anniversaire', 'Anniversaire'),
    ('Fiançailles', 'Fiançailles'),
    ('Réunion de famille ou amis', 'Réunion de famille ou amis'),
    ('Soirée à thème', 'Soirée à thème'),
    ('Soutenance', 'Soutenance'),
    ('Conférence', 'Conférence'),
    ('Autre', 'Autre')
]

SERVICES_TYPES = [
    ('Animation musicale', 'Animation musicale'),
    ('Photos et vidéos', 'Photos et vidéos'),
    ('Beauté et coiffure', 'Beauté et coiffure'),
    ('Location de matériel', 'Location de matériel'),
    ('Soirée à thème', 'Soirée à thème'),
    ('Traiteur', 'Traiteur'),
    ('Location de salles', 'Location de salles')
]



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
        choices=CLIENT_TYPES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user


class Service(models.Model):
    nom_service = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        choices=SERVICES_TYPES)
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
        return self.service

class ImageServicePartenaire(models.Model):
    service_partenaire = models.ForeignKey(
        ServicePartenaire,
        on_delete=models.CASCADE,
        null=False,
        blank=False)
    image = models.ImageField(upload_to ='uploads/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.service_partenaire


class Evenement(models.Model):
    nom_evenement = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        choices=EVENEMENT_TYPES)

    def __str__(self):
        return self.nom_evenement


class EvenementClient(models.Model):
    client_profile = models.ForeignKey(
        ClientProfile,
        on_delete=models.CASCADE,
        null=False,
        blank=False)
    evenement = models.ForeignKey(
        Evenement,
        on_delete=models.CASCADE,
        null=False,
        blank=False)
    nombre_invites = models.PositiveIntegerField(null=False, null=False, default=1)
    date = models.DateTimeField(null=False, null=False)
    ville = models.DateField(null=False, null=False)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.evenement
    

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

    def __str__(self):
        return self.evenement_client


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

    def __str__(self):
        return self.evenement_client