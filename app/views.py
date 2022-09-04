# IMPORTATION GENERAL
from http import client
import json
from xml.dom import UserDataHandler
from datetime import date, datetime
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
import app.m00_common as m00

def accueil(request):
    template = "index.html"
    if request.user and not request.user.is_superuser:
        type_client = am.ClientProfile.objects.get(
            user=request.user).type_client
        if type_client == 'Client':
            return redirect('creer_evenement')
        elif type_client == 'Partenaire':
            return redirect('liste_evenements')
        else:
            pass
    return render(request, template, {})



#######################################################################################
#######################################################################################
#######################################################################################
# authentification  && utilisateurs
#######################################################################################
#######################################################################################
#######################################################################################
def login(request, type_client):
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
                        client=am.ClientProfile.objects.get(user=user)
                        if client.type_client == 'Partenaire':
                            return redirect('liste_evenements')
                        else:
                            return redirect('creer_evenement')
                        
                    else:
                       return render(request, template, {'login_form': login_form,'error_message': "Vous avez entré un email ou un mot de passe invalide"})
            else:
                return render(request, template, {'login_form': login_form,'error_message': "Vous avez entré un email ou un mot de passe invalide"})      
    return render(request, template, {'login_form':login_form, 'user':user})
   

def register(request, type_client):
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
                    email=signup_form.cleaned_data['email'],
                    password=signup_form.cleaned_data['password_repeat'],
                    first_name=signup_form.cleaned_data['user_name'],
                    username=signup_form.cleaned_data['email']
                )
                user.save()
                #creation de client
                ville = signup_form.cleaned_data['ville']
                telephone = signup_form.cleaned_data['telephone']                
                client = am.ClientProfile()
                client.telephone_mobile=telephone
                client.ville = ville
                client.type_client = type_client
                client.user = user
                
                client.save()                
                user = authenticate(
                    request , username=signup_form.cleaned_data['email'],
                     password=signup_form.cleaned_data['password_repeat'])
                auth_login(request, user)
                if client.type_client == 'Partenaire':
                    return redirect('liste_evenements')
                else:
                    return redirect('creer_evenement')
        else:
            print(signup_form.errors)     
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
            print(email)
            if User.objects.filter(email=email).exists():
                    user = User.objects.get(email=email)
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


def liste_evenements(request):
    """
    la fonction qui permet de lister les evenements qui concernent un
    utilisateur
    """

    template = 'partenaire/index.html'
    user = request.user
    partenaire = am.ClientProfile.objects.get(user=user)
    services_partner = am.ServicePartenaire.objects.all()
    services = am.ServiceEvenement.objects.all()

    return render(request, template, {"services": services})


def creer_evenement(request):
    """
    la fonction creer evenement pour creer un evenement
    """

    types_evenements = m00.EVENEMENT_TYPES
    types_services = am.Service.objects.all()
    villes_maroc = m00.VILLES_MAROC
    context = {
        "types_evenements": types_evenements,
        "types_services": types_services,
        "villes_maroc": villes_maroc
    }
    return render(request, 'evenement/create-evenement.html', context)


def ajax_calls(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        action = received_json_data['action']

        if action == "creer_evenement":

            nv_evenement = am.EvenementClient()
            nv_evenement.client_profile = request.user.client_profile
            nv_evenement.type_evenement = received_json_data['type_evenement']
            nv_evenement.nombre_invites = received_json_data['invitations']
            nv_evenement.date = datetime.strptime(str(received_json_data['date_evenement']), "%m/%d/%Y")
            nv_evenement.ville = received_json_data['ville']

            nv_evenement.save()
            data_dict = {"nv_evenement_id": nv_evenement.id}

        if action == "creer_services_evenement":

            nv_evenement_id = received_json_data['nv_evenement_id']

            nv_service_evenement = am.ServiceEvenement()
            nv_service_evenement.evenement_client =\
                am.EvenementClient.objects.get(id=nv_evenement_id)
            nv_service_evenement.service = am.Service.objects.get(
                id=received_json_data['type_service'])
            nv_service_evenement.description = received_json_data['description']
            nv_service_evenement.save()
            data_dict = {}

    return JsonResponse(data=data_dict, safe=False)
