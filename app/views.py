from django.shortcuts import render

# Create your views here.

def accueil(request):
    template = "index.html"
    return render(request, template, {})