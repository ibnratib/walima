# IMPORTATION GENERAL
import json
from xml.dom import UserDataHandler

# IMPORTATION DJANGO
from django.shortcuts import render, redirect, HttpResponse
from django.utils.http import urlsafe_base64_encode
from django.http import JsonResponse
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, logout, login as auth_login
from django.template.loader import render_to_string
from django.contrib.auth.models import User


# IMPORTATION APP
import app.forms as af
import app.models as am


def accueil(request):
    template = "index.html"
    return render(request, template, {})



#######################################################################################
#######################################################################################
#######################################################################################
# authentification  && utilisateurs
#######################################################################################
#######################################################################################
#######################################################################################
def login(request):
    template = 'auth/login.html'
    login_form = af.LoginForm()
    error_message = ''
    user = request.user

    if request.method == 'POST':
        login_form = af.LoginForm(request.POST)
        if login_form.is_valid():
            # recuperation des informations de login
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            #verifier l existance de l'utilisateur et leur information d'authentification
            if  User.objects.filter(email=email).exists():
                    user = authenticate(request , username=email, password=password)
                    if user is not None and user.is_active:
                        auth_login(request, user)
                        return redirect('/')
                    else:
                       return render(request, template, {'login_form': login_form,'error_message': "Vous avez entré un email ou un mot de passe invalide"})
            else:
                return render(request, template, {'login_form': login_form,'error_message': "Vous avez entré un email ou un mot de passe invalide"})      
    return render(request, template, {'login_form':login_form, 'user':user})
   

def register(request):
    template = 'auth/register.html'
    error_message = ''
    signup_form = af.RegistreForm() 
    if request.method == 'POST':
        signup_form = af.RegistreForm(request.POST,request.FILES)
        if signup_form.is_valid():
            #verifier l existance de l'utilisateur
            if User.objects.filter(email=signup_form.cleaned_data['email']).exists():
                return render(request, template, {
                    'signup_form': signup_form,
                    'error_message': 'Cet email est déja utilisé'
                })
            #verifier si les mots de passe nes sont pas identiques
            else:
                #creation d'utilisteur
                user = User.objects.create_user(
                    signup_form.cleaned_data['email'],
                    signup_form.cleaned_data['password'],
                    signup_form.cleaned_data['user_name'],
                )
                user.save()
                #creation de pharmacie
                ville = signup_form.cleaned_data['ville']
                telephone = signup_form.cleaned_data['telephone']                
                pharmacie = am.ClientProfile()
                pharmacie.telephone_mobile=telephone
                pharmacie.ville = ville
                pharmacie.save()
                pharmacie.user = user
                pharmacie.save()
                
                user = authenticate(
                    request , username=signup_form.cleaned_data['email'],
                     password=signup_form.cleaned_data['password'])
                
        signup_form = af.RegistreForm()
    return render(request,template,{'signup_form':signup_form}) 


def reset_password(request):
    '''
    This is the view to set a new password
    '''
    form = af.ResetPasswordForm()
    if request.method == 'POST':
        form = af.ResetPasswordForm(request.POST,request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            if am.ClientProfile.objects.filter(email=form.cleaned_data['email']).exists():
                    user = am.ClientProfile.objects.get(email=email)
                    subject = "Password Reset Requested"
                    email_template_name = "auth/reset-password-email.html"
                    c = {
                    "email":user.email,
                    'domain':'http://localhost:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': 'https',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'ibnouratib.pro@gmail.com' , [user.email], fail_silently=False,)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')

                    return render(request, 'auth/reset-password-sent.html', {})
            else:

                return render(request, 'auth/reset-password.html', {
                    'form': form,
                    'error_message': 'Vous avez entré un email invalide'
                })
                
    return render(request, 'auth/reset-password.html', {'form': form})
def reset_password_sent(request):
    """
    la fonction resset_password_done notifier l'utilisateur que l'email de
    reset password est envoye
    """
    context={}
    return render(request, 'auth/reset-password-sent.html', context)

def logout_view(request):
    """
    la fonction logout_view permet à un utilisateur de se déconnecter
    """
    logout(request)
    return redirect('/login')
