# Generated by Django 4.0.3 on 2022-08-15 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EasyJobMakerApp', '0011_job_application'),
    ]

    operations = [
        migrations.AddField(
            model_name='job_application',
            name='service_provider_image',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
