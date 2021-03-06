from distutils.command.upload import upload
from operator import truth
from pickle import TRUE
from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    image = models.FileField(null = True, blank = True, upload_to = '')

    def __str__(self):
        return self.full_name
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = '../../static/images/avatar.png'
        return url    


class Service_Provider(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name

class Job_Location(models.Model):
    city = models.CharField(max_length=30, blank=True, null=True)
    region = models.CharField(max_length=30, null=True)
    def __str__(self):
        return self.city

class Job(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    job_title = models.CharField(max_length=100, null=True)
    contact_name= models.CharField(max_length=200, null=True)
    contact_phone=models.CharField(max_length=10, null=True)
    job_description=models.CharField(max_length=1000, null=True)
    date_added = models.DateTimeField(auto_now_add=True,  blank = True)
    complete = models.BooleanField(default=False,  blank = True)
    in_progress = models.BooleanField(default=False,  blank = True)
    transaction_id = models.CharField(max_length=100, null=True)
    service_provider = models.ForeignKey(Service_Provider, on_delete=models.SET_NULL, null=True, blank=True)
    job_completion_time = models.DateTimeField(null=True, blank = True)
    payment_for_job = models.FloatField(null=True, blank = True)
    image = models.FileField(null = True, blank = True, upload_to = '')

    def __str__(self):
        return str(self.job_title)


    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = '../../static/images/defaulet_job.jpg'
        return url


class Job_Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)



    def __str__(self):
        return self.address




# Create your models here.
