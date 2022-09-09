import app.models as am
import pandas as pd
from django.db import connection

def annonces_compe_client(client_profile: am.ClientProfile):

    if client_profile.type_client == "Partenaire":

        query = '''
        select id, type_evenement, ville, date, nom_service, case when unread_messages is null then 0 else unread_messages end as unread_messages from (
        select * from (      
            select 
                available_annonces.id,
                available_annonces.type_evenement,
                available_annonces.client_profile_id,
                available_annonces.ville,
                available_annonces.nombre_invites,
                available_annonces.date,
                available_annonces.service_id,
                available_annonces.nom_service
                
            from app_servicepartenaire join 

            (
                select
                    app_evenementclient.type_evenement,
                    app_evenementclient.client_profile_id,
                    app_evenementclient.nombre_invites,
                    app_clientprofile.ville,
                    app_evenementclient.date,
                    app_serviceevenement.id,
                    app_serviceevenement.service_id,
                    app_service.nom_service
                from
                    app_serviceevenement
                join
                    app_evenementclient
                on
                    app_evenementclient.id=app_serviceevenement.evenement_client_id
                join
                    app_service
                on
                    app_service.id=app_serviceevenement.service_id
                join
                    app_clientprofile
                on
                    app_clientprofile.id=app_evenementclient.client_profile_id)
                as available_annonces
                    
            on app_servicepartenaire.service_id = available_annonces.service_id

            where app_servicepartenaire.client_profile_id=''' + str(client_profile.id) + ''') as my_annonces


            join (

                select
                    sum(case when (message_read=0 or message_read='false') then 1 else 0 end) as unread_messages, sum(case when (message_read=1 or message_read='true') then 1 else 0 end) as read_messages, service_evenement_id
                from
                    app_messageservice
                where
                    message_receiver_id = ''' + str(client_profile.id) + '''
                group by service_evenement_id)
                as my_unread_messages

            on my_unread_messages.service_evenement_id=my_annonces.id) as my_annonces_and_messages

            '''

    elif client_profile.type_client == "Client":

        query = '''
        select id, type_evenement, ville, date, nom_service, case when unread_messages is null then 0 else unread_messages end as unread_messages, case when read_messages is null then 0 else read_messages end as read_messages from (
        select * from (   
            select
                app_evenementclient.type_evenement,
                app_evenementclient.client_profile_id,
                app_evenementclient.nombre_invites,
                app_clientprofile.ville,
                app_evenementclient.date,
                app_serviceevenement.id,
                app_serviceevenement.service_id,
                app_service.nom_service
            from
                app_serviceevenement
            join
                app_evenementclient
            on
                app_evenementclient.id=app_serviceevenement.evenement_client_id
            join
                app_service
            on
                app_service.id=app_serviceevenement.service_id
            join
                app_clientprofile
            on
                app_clientprofile.id=app_evenementclient.client_profile_id
            where client_profile_id=''' + str(client_profile.id) + ''') as my_annonces


            left outer join (

                select
                    sum(case when (message_read=0 or message_read='false') then 1 else 0 end) as unread_messages, sum(case when (message_read=1 or message_read='true') then 1 else 0 end) as read_messages, service_evenement_id
                from
                    app_messageservice
                where
                    message_receiver_id = ''' + str(client_profile.id) + '''
                group by service_evenement_id)
                as my_unread_messages

            on my_unread_messages.service_evenement_id=my_annonces.id) as my_annonces_and_messages

            '''

    df = pd.read_sql_query(query, connection)

    dict_df = df.to_dict('records')

    return dict_df