# Generated by Django 4.0.3 on 2022-08-10 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EasyJobMakerApp', '0006_alter_reviewrating_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewrating',
            name='job',
            field=models.ForeignKey(default=22, on_delete=django.db.models.deletion.CASCADE, to='EasyJobMakerApp.job'),
            preserve_default=False,
        ),
    ]
