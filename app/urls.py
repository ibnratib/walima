from django.urls import path

import app.views as av
from django.contrib.auth import views as auth_views


urlpatterns=[
    path("", av.accueil, name="accueil"),
    path("evenements", av.list_evenements, name="list_evenements"),
    
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #//////////////////////////////////////////////AUTHENTIFICATIONS//////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #//////////////////////////////////////////////////////////////////////////////////////////////////////////////// 

    path("login/<str:type_client>", av.login,name='login'),
    path("inscription/<str:type_client>", av.register,name='register'),
    path('log-out/', av.logout_view, name="logout_view"),
    path('reset-password/', av.reset_password, name='reset_password'),
    path('reset-password-sent/', av.reset_password_sent, name='reset_password_sent'),
    path('reset-password-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='auth/reset-password-confirm.html'),name='reset_password_confirm'),    
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/reset-password-complete.html'),name='password_reset_complete'),

    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #//////////////////////////////////////////////EVENEMENTS//////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    path("creer-evenement/", av.creer_evenement, name='creer_evenement'),
    path("services-partenaire/", av.partenaire_service, name='partenaire_service'),
    path("creer-service-partenaire/", av.ajouter_service_partenaire, name='ajouter_service_partenaire'),
    

    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #//////////////////////////////////////////////AJAX//////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #//////////////////////////////////////////////////////////////////////////////////////////////////////////////// 

    path("ajax-calls/", av.ajax_calls,name='ajax_calls'),
]
