from django.db import models
from datetime import date, timedelta

# Create your models here.
#class doner(models.Model):
    fname=models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    dist=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    phone=models.CharField(max_length=20)
    email=models.CharField(max_length=50)
    age=models.IntegerField()
    gender=models.CharField(max_length=20)
    bgroup=models.CharField(max_length=20)
    ldate=models.DateField()
    allergy=models.CharField(max_length=50, default='Nil')
    photo=models.ImageField(upload_to='images/')
    uname=models.CharField(max_length=100)
    pword=models.CharField(max_length=100)
    rights=models.CharField(max_length=20,default='New Doner')
    status=models.CharField(max_length=25,default='Active')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import doner  # your model name
from datetime import datetime

def donerreg(request):
    if request.method == 'POST':
        try:
            fname = request.POST.get('t1')
            lname = request.POST.get('t2')
            address = request.POST.get('t3')
            dist = request.POST.get('t4')
            city = request.POST.get('t5')
            phone = request.POST.get('t6')
            email = request.POST.get('t7')
            age = request.POST.get('t8')
            gender = request.POST.get('t9')
            bgroup = request.POST.get('t10')
            ldate = request.POST.get('t11')
            allergy = request.POST.get('t12', 'Nil')  # Default value if not provided
            disease = request.POST.get('t13', 'Nil')
            uname = request.POST.get('t14')
            pword = request.POST.get('t15')

            # Safely get uploaded photo (will be None if not uploaded)
            photo = request.FILES.get('file')
            if not photo:
                messages.error(request, "Please upload a photo.")
                return redirect('/dr/')  # or use named URL pattern

            new_doner = doner(
                fname=fname,
                lname=lname,
                address=address,
                dist=dist,
                city=city,
                phone=phone,
                email=email,
                age=age,
                gender=gender,
                bgroup=bgroup,
                ldate=ldate,
                allergy=allergy,
                photo=photo,
                uname=uname,
                pword=pword,
            )

            new_doner.save()
            messages.success(request, "Donor registration successful. Please wait for admin approval.")
            return redirect('/dr/')  # or your desired success page

        except Exception as e:
            print("Error in donor registration:", e)
            messages.error(request, "Something went wrong. Please try again.")
            return redirect('/dr/')
    
    return render(request, 'donerreg.html')

class patient(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    uname = models.CharField(max_length=100, unique=True)
    pword = models.CharField(max_length=100)
    rights=models.CharField(max_length=15,default='user')

class stock(models.Model):
    bgroup=models.CharField(max_length=50)
    qty=models.IntegerField(default=0)

class bloodrequest(models.Model):
    reqno=models.IntegerField()
    rdate=models.DateField(default=date.today)
    pid=models.IntegerField()
    pname=models.CharField(max_length=50)
    pphone=models.CharField(max_length=50)
    bg=models.CharField(max_length=50)
    reqdate=models.DateField()
    did=models.IntegerField()
    dname=models.CharField(max_length=50)
    dphone=models.CharField(max_length=20)
    msg=models.CharField(max_length=150)
    status=models.CharField(max_length=20,default='New Request')

class directrequest(models.Model):
    reqno=models.IntegerField()
    pid=models.IntegerField()
    pname=models.CharField(max_length=100)
    phone=models.CharField(max_length=20)
    bg=models.CharField(max_length=50)
    rdate=models.DateField()
    details=models.CharField(max_length=150)
    nofb=models.IntegerField()
    status=models.CharField(max_length=25,default='New Request')

class feedback(models.Model):
    pid=models.IntegerField()
    pname=models.CharField(max_length=50)
    did=models.IntegerField()
    msg=models.CharField(max_length=150)

class notification(models.Model):
    venue=models.CharField(max_length=100)
    purpose=models.CharField(max_length=100)
    pdate=models.DateField()
    ptime=models.CharField(max_length=50)
    note=models.CharField(max_length=250)





