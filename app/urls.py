from django.urls import path

import app.views as av

urlpatterns=[
    path("", av.accueil, name="accueil")
    ]
