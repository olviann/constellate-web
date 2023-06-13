from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date, datetime
import pytz
from geopy.geocoders import ArcGIS
from geopy.geocoders import Nominatim
from kerykeion import print_all_data, KrInstance
from django.urls import reverse
from .models import Client

@login_required(login_url='login')
def HomePage(request):
    if request.method=='POST':
        input_name=request.POST.get('name')
        input_birthdate=request.POST.get('date')
        input_birthtime=request.POST.get('time')
        input_birthplace=request.POST.get('place')
        str_date_time = input_birthdate + ' ' + input_birthtime
        dt_date_time=datetime.strptime(str_date_time, '%d/%m/%Y %H:%M')
        locator = Nominatim(user_agent="myGeocoder")
        location = locator.geocode(input_birthplace)
        utc_dt = dt_date_time.astimezone(pytz.utc)
        calculations = KrInstance(input_name,dt_date_time.year, dt_date_time.month, dt_date_time.day,
                             dt_date_time.hour,dt_date_time.minute,input_birthplace, location.latitude, location.longitude)
        sun_sign = getattr(calculations.sun,"sign" )
        moon_sign = getattr(calculations.moon,"sign" )
        mercury_sign = getattr(calculations.mercury,"sign" )
        venus_sign = getattr(calculations.venus,"sign" )
        mars_sign = getattr(calculations.mars,"sign" )
        jupiter_sign = getattr(calculations.jupiter,"sign" )
        saturn_sign = getattr(calculations.saturn,"sign" )
        Profile_instance = Client.objects.all()
        client = {
            "name": Profile_instance
        }
        return render(request, 'results.html', client)
    else:
     return render(request, 'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        
        if pass1!=pass2:
            messages.success(request,"Passwords do not match")
        else:
            my_user=User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')
    return render(request, 'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,"Incorrect username/password")

    return render(request, 'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def ResultsPage(request):
    #parsed_sign_of_planets = request.session['sign_of_planets']
    #print(sign_of_planets)
    return render (request, 'results.html')

def handler400(request, exception):
    return (render(request, "400.html", status=400))

def handler403(request, exception):
    return (render(request, "403.html", status=403))

def handler404(request, exception):
    return (render(request, "404.html", status=404))

def handler500(request):
    return (render(request, "500.html", status=500))
