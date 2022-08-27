# IMPORTATION GENERAL

# IMPORTATION DJANGO
from django.contrib import admin

# IMPORTATION APP
import app.models as am

# Register your models here.

@admin.register(am.ClientProfile)
class ClientAdmin(admin.ModelAdmin):
    pass

@admin.register(am.Service)
class ServiceAdmin(admin.ModelAdmin):
    pass

@admin.register(am.ServicePartenaire)
class ServicePartenaireAdmin(admin.ModelAdmin):
    pass

@admin.register(am.ServiceEvenement)
class ServiceEvenementAdmin(admin.ModelAdmin):
    pass

@admin.register(am.MessageService)
class MessageServiceAdmin(admin.ModelAdmin):
    pass

@admin.register(am.EvenementClient)
class EvenementClientAdmin(admin.ModelAdmin):
    pass

