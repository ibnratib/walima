# Generated by Django 3.2.4 on 2022-09-09 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20220905_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='messageservice',
            name='message_read',
            field=models.BooleanField(default=False),
        ),
    ]
