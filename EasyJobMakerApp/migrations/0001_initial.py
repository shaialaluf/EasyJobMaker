# Generated by Django 3.2.6 on 2022-04-29 07:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(max_length=200)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=100, null=True)),
                ('contact_name', models.CharField(max_length=200, null=True)),
                ('contact_phone', models.CharField(max_length=10, null=True)),
                ('job_description', models.CharField(max_length=1000, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(blank=True, default=False)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True)),
                ('transaction_id', models.CharField(max_length=100, null=True)),
                ('job_completion_time', models.DateTimeField(blank=True, null=True)),
                ('payment_for_job', models.FloatField(blank=True, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='EasyJobMakerApp.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Job_Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(blank=True, max_length=30, null=True)),
                ('region', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service_Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(max_length=200)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Job_Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('zipcode', models.CharField(max_length=200)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='EasyJobMakerApp.customer')),
                ('job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='EasyJobMakerApp.job')),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='service_provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='EasyJobMakerApp.service_provider'),
        ),
    ]
