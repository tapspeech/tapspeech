# Generated by Django 3.2.4 on 2021-06-24 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tapSpeech_app', '0005_alter_requests_request_patient'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='emergencyContact',
            field=models.CharField(default='', max_length=30),
        ),
    ]
