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
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import CharField, Value

# IMPORTATION APP
import app.forms as af
import app.models as am
import app.m00_common as m00
import app.queries as aq

def accueil(request):
    template = "index.html"
    try:
        if request.user:
            if not request.user.is_superuser:
                type_client = am.ClientProfile.objects.get(
                    user=request.user).type_client
                if type_client == 'Client':
                    return redirect('creer_evenement')
                elif type_client == 'Partenaire':
                    return redirect('liste_services')
                else:
                    pass
    except:
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
                            return redirect('liste_services')
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
    print(type_client)
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
                    return redirect('liste_services')
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
    return redirect('/')


@login_required(login_url='/')
def liste_services(request):
    """
    la fonction qui permet de lister les evenements qui concernent un
    utilisateur
    """

    template = 'partenaire/index.html'
    services = aq.annonces_compe_client(request.user.client_profile)

    print(services)
    return render(request, template, {"services": services})

@login_required(login_url='/')
def detail_service(request, pk):
    """
    Ici, les clients et partenaires peuvent consulter le détail d'un service
    demandé avec possibilité de discussion
    """

    service = am.ServiceEvenement.objects.get(id=pk)
    template = 'services/details.html'
    return render(request, template, {"service": service})

@login_required(login_url='/')
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

@login_required(login_url='/')
def ajax_calls(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        action = received_json_data['action']

        if action == "envoyer_message_sur_evenement":

            nv_message = am.MessageService()
            nv_message.service_evenement = am.ServiceEvenement.objects.get(
                id=received_json_data['service'])
            nv_message.message_sender = am.ClientProfile.objects.get(
                id=received_json_data['sender'])
            nv_message.message_receiver = am.ClientProfile.objects.get(
                id=received_json_data['receiver'])
            nv_message.message = received_json_data['message']
            nv_message.save()
            data_dict = {}

        if action == "get_messages_service":

            service = am.ServiceEvenement.objects.get(
                id=received_json_data['service'])
            
            if int(received_json_data['other_person']) == 0:
                other_person = request.user.client_profile

                messages = am.MessageService.objects.filter(
                    (Q(message_sender=request.user.client_profile.id) | Q(message_receiver = request.user.client_profile.id)),
                    service_evenement=service
                    )
                list_of_senders = list(set([m.message_sender for m in messages]))
                messages=[]

               #mark messages as read
                am.MessageService.objects.filter(
                                    message_receiver = request.user.client_profile,
                                    service_evenement=service).update(
                                        message_read=True)

            else:
                other_person = am.ClientProfile.objects.get(
                    id=received_json_data['other_person'])
                messages = am.MessageService.objects.filter(
                    (Q(message_sender=request.user.client_profile.id) | Q(message_receiver = request.user.client_profile.id)),
                    (Q(message_sender=other_person) | Q(message_receiver = other_person)),
                    service_evenement=service
                    )
                list_of_senders = list(set([m.message_sender for m in messages]))

                #mark messages as read
                am.MessageService.objects.filter(
                                    message_receiver = request.user.client_profile,
                                    message_sender=other_person,
                                    service_evenement=service).update(
                                        message_read=True)

            if len(list_of_senders) == 0 and request.user.client_profile.type_client == "Client":
                list_of_senders = ["Aucun interessé pour le moment"]
                
            html_senders = render_to_string(
                template_name="services/liste-senders.html",
                context={
                    "list_of_senders": list_of_senders,
                    "client_profile": request.user.client_profile}
                )

            html_conversation = render_to_string(
                template_name="services/chat-area.html",
                context={
                    "messages": messages,
                    "client_profile": request.user.client_profile}
                )

            data_dict = {
                "html_conversation": html_conversation,
                "html_senders": html_senders
                }

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
        if action == 'supprimer_service':
            id = received_json_data['id']
            am.ServicePartenaire.objects.filter(id=id).delete()
            data_dict = {}

    return JsonResponse(data=data_dict, safe=False)


@login_required(login_url='/')
def partenaire_service(request):
    template = 'services/services-partenaire.html'
    client_profile = am.ClientProfile.objects.get(user=request.user)
    type_client = client_profile.type_client
    liste_services = am.ServicePartenaire.objects.filter(
        client_profile=client_profile)
    return render(request, template,{
        "liste_services": liste_services,
        'type_client': type_client
        })

@login_required(login_url='/')
def ajouter_service_partenaire(request):
    template = 'services/ajouter-service-partenaire.html'
    form = af.ServicePartenaireForm()

    client_profile = am.ClientProfile.objects.get(user=request.user)
    type_client = client_profile.type_client
    if request.method == 'POST':
        form = af.ServicePartenaireForm(request.POST ,request.FILES)
        if form.is_valid():
            service = form.cleaned_data['service']
            description = form.cleaned_data['description_de_service']

            if am.ServicePartenaire.objects.filter(
                client_profile=client_profile, service=service).exists():
                return render(request, template,{
                    'form': form, "message_error": "le service existe déjà !",
                    'type_client': type_client})
            service_partenaire = am.ServicePartenaire()
            service_partenaire.client_profile = client_profile
            service_partenaire.service = service
            service_partenaire.description = description
            service_partenaire.save()
            for image in request.FILES.getlist('images_de_service'):
                am.ImageServicePartenaire.objects.create(
                    image=image,
                    service_partenaire=service_partenaire)
            return redirect('/services-partenaire')
            
        else:
            print(form.errors)
    return render(request, template,{
        'form': form,'type_client': type_client})