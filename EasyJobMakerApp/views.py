from contextvars import Context
from email.mime import image
from http.client import HTTPResponse
from multiprocessing import Event, context
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import datetime
import json
import os
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib import messages
import csv
from .forms import CreateUserForm
from django.template import context,loader




def main(request):
    if request.user.is_authenticated:  
        try: 
            service_provider = Service_Provider.objects.get(user = request.user)
            is_service_provider = True
        except Service_Provider.DoesNotExist:
            is_service_provider = False
    else:
        is_service_provider = False    
    context = {"is_service_provider":is_service_provider}
    return render(request, "EasyJobMakerApp/main.html", context)


def jobs(request):
    jobs = Job.objects.all()
    if request.user.is_authenticated:
        try: 
            service_provider = Service_Provider.objects.get(user = request.user)
            is_service_provider = True
        except Service_Provider.DoesNotExist:
            is_service_provider = False

    else:
        is_service_provider = False
        
    context = {'jobs': jobs, 'is_service_provider': is_service_provider}
    return render(request, "EasyJobMakerApp/jobs.html", context)

def jobsToDo(request):
    service_provider=Service_Provider.objects.get(user = request.user)
    my_jobs=Job.objects.filter(service_provider=service_provider)
    
    
    return render(request, "EasyJobMakerApp/jobsToDo.html", {'jobs': my_jobs,"is_service_provider":True})

def myJobs(request):
    customer=Customer.objects.get(user = request.user)
    my_jobs=Job.objects.filter(customer=customer)
    if request.user.is_authenticated:  
        try: 
            service_provider = Service_Provider.objects.get(user = request.user)
            is_service_provider = True
        except Service_Provider.DoesNotExist:
            is_service_provider = False
    else:
        is_service_provider = False    
    
    return render(request, "EasyJobMakerApp/myJobs.html", {'jobs': my_jobs,"is_service_provider":is_service_provider})

def checkout(request,job_id):
    job = get_object_or_404(Job, id=job_id)
    jobAddress=get_object_or_404(Job_Address,job=job)
    #return render(request, 'EasyJobMakerApp/jobDetails.html', {'job': job,'jobAddress':jobAddress})
    return render(request, "EasyJobMakerApp/checkout.html", {'job': job,'jobAddress':jobAddress})


def jobDetails(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    jobAddress=get_object_or_404(Job_Address,job=job)
    return render(request, 'EasyJobMakerApp/jobDetails.html', {'job': job,'jobAddress':jobAddress})



def jobBuilder(request):
    jobsLocations = Job_Location.objects.all()
    if request.user.is_authenticated:    
        try: 
            service_provider = Service_Provider.objects.get(user = request.user)
            is_service_provider = True
        except Service_Provider.DoesNotExist:
            is_service_provider = False
    else:
            is_service_provider = False    


    context = {'jobsLocations': jobsLocations,"is_service_provider":is_service_provider}
    return render(request, "EasyJobMakerApp/jobBuilder.html", context)


def addJob(request):
    transaction_id = datetime.datetime.now().timestamp()
    userData = json.loads(request.POST.get('userFormData'))['userData']
    jobDetails =  json.loads(request.POST.get('jobDetails'))['jobDetails']
    shipping =  json.loads(request.POST.get('shippingInfo'))['shipping']
    
    if request.user.is_authenticated:    
   
        customer = Customer.objects.get(user=request.user)
        contact_name = userData['name']
        contact_phone = userData['phone']
        job_title = jobDetails['jobTitle']
        job_description = jobDetails['jobDescription']
        payment_for_job = jobDetails['jobPayment']
        job_image = request.FILES.get('image')
        job_address = shipping['address']
        job_city = shipping['city']
        job_state = shipping['state']
        job_zipcode = shipping['zipcode']
        new_job = Job.objects.create(customer = customer, contact_name = contact_name, contact_phone = contact_phone,job_title = job_title, job_description = job_description, transaction_id = transaction_id
        ,payment_for_job = payment_for_job, image = job_image)

        Job_Address.objects.create(customer = customer, job = new_job, address = job_address, city = job_city, state =  job_state, zipcode = job_zipcode)
    context={}
  
    return render(request, "EasyJobMakerApp/jobBuilder.html", context)

def registerPage(request):
    form = CreateUserForm()
    context = {'form': form}
    return render(request, "EasyJobMakerApp/register.html", context)

def loginPage(request):
    context = {}
    return render(request, "EasyJobMakerApp/login.html", context)

def makelogin(request):
    # if request.user.is_authenticated:
    #     return redirect('jobs')
    # else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                return redirect("jobs")
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'EasyJobMakerApp/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('loginPage')


def makeRegister(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    # else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                user_name = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user_name)

                full_name = form.cleaned_data.get('first_name') + ' ' + form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('email')
                new_customer = Customer(user = user, full_name = full_name, email = email)
                new_customer.save()
                if request.POST.get('service_provider') == 'on':
                    new_service_provider = Service_Provider(user = user, full_name = full_name, email = email)
                    new_service_provider.save()
                return redirect('loginPage')

        context = {'form': form}
        return render(request, 'EasyJobMakerApp/register.html', context)
# Create your views here.

def takeJob(request):
    data = json.loads(request.body)
    job_id = data['Job_Id']
    job = get_object_or_404(Job, id=job_id)
    job.in_progress = True
    service_provider = Service_Provider.objects.get(user = request.user)
    job.service_provider = service_provider
    job.save()
    return render(request, 'EasyJobMakerApp/jobs.html')


def myProfile(request):
    current_user = Customer.objects.get(user = request.user)
    try: 
        service_provider = Service_Provider.objects.get(user = request.user)
        is_service_provider = True
    except Service_Provider.DoesNotExist:
        is_service_provider = False
    return render(request, 'EasyJobMakerApp/myProfile.html', {'customer': current_user, 'is_service_provider': is_service_provider})


def search(request):
    query = request.GET.get('query', '')
    if query:
        jobs = Job.objects.filter(Q(job_title__icontains=query))
    else :
        jobs=Job.objects.all()
    if request.user.is_authenticated:
        try:
            service_provider = Service_Provider.objects.get(user = request.user)
            is_service_provider = True
        except Service_Provider.DoesNotExist:
            is_service_provider = False

    else:
        is_service_provider = False        
    context = {'jobs': jobs, 'is_service_provider': is_service_provider}

    return render(request, 'EasyJobMakerApp/jobs.html', context)


def filteredJobsByRegion(request):
    region = json.loads(request.POST.get('Region'))['region']
    if region != "All Regions":
                
        jobLocation=Job_Location.objects.filter(region=region)
        temp_cities=list(jobLocation.values_list("city"))
        cities =[]
        for city in temp_cities:
            cities.append(str(city)[2:-3])
        job_addr=Job_Address.objects.filter(city__in=cities)
        jobs_str =[]
        for job in job_addr.values_list("job"):
            jobs_str.append(str(job)[1:-2])

        jobs=Job.objects.filter(id__in=jobs_str)

    
    
    else:
        jobs=Job.objects.all()
    if request.user.is_authenticated:
        try:
            service_provider = Service_Provider.objects.get(user = request.user)
            is_service_provider = True
        except Service_Provider.DoesNotExist:
            is_service_provider = False

    else:
        is_service_provider = False        
    context = {'jobs': jobs, 'is_service_provider': is_service_provider}
    template = loader.get_template('EasyJobMakerApp/jobs.html')
    html = template.render(context)
    
    # c= Context({'jobs': jobs, 'is_service_provider': is_service_provider})
    return HttpResponse(html)
    # return render(request, "EasyJobMakerApp/jobs.html", context)





def updateProfile(request):
    userChoiceServiceProvider = json.loads(request.POST.get('ServiceProvider'))['isServiceProvider']
    customer = Customer.objects.get(user=request.user)
    profile_image = request.FILES.get('image')
    if profile_image:
        customer.image=profile_image
        customer.save()

    try: 
        service_provider = Service_Provider.objects.get(user = request.user)
        is_service_provider = True
    except Service_Provider.DoesNotExist:
        is_service_provider = False
    
    if is_service_provider:
        if  userChoiceServiceProvider==False:
            Job.objects.filter(service_provider=service_provider,in_progress=True).update(in_progress=False)
            service_provider.delete()
    else:
        if  userChoiceServiceProvider==True:
            new_service_provider = Service_Provider(user = request.user, full_name = customer.full_name, email = customer.email)
            new_service_provider.save()
    context = {}
    return render(request, "EasyJobMakerApp/myProfile.html", context)

        
