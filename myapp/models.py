from django.db import models
from datetime import date

# ----------------------
# Doner model
# ----------------------
class doner(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    dist = models.CharField(max_length=100)  # Changed from 'district' to 'dist'
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)  # Changed to EmailField
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    bgroup = models.CharField(max_length=20)
    ldate = models.DateField()
    allergy = models.CharField(max_length=50, default='No')
    disease = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='donor_photos/')
    uname = models.CharField(max_length=100, unique=True)
    pword = models.CharField(max_length=128)  # Increased length for hashed passwords
    rights = models.CharField(max_length=20, default='New Doner')
    status = models.CharField(max_length=25, default='Active')

    def __str__(self):
        return f"{self.fname} {self.lname}"

# ----------------------
# Patient model
# ----------------------
class patient(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    uname = models.CharField(max_length=100, unique=True)
    pword = models.CharField(max_length=100)
    rights = models.CharField(max_length=15, default='user')

# ----------------------
# Stock model
# ----------------------
class stock(models.Model):
    bgroup = models.CharField(max_length=50)
    qty = models.IntegerField(default=0)

# ----------------------
# Blood Request model
# ----------------------
class bloodrequest(models.Model):
    reqno = models.IntegerField()
    rdate = models.DateField(default=date.today)
    pid = models.IntegerField()
    pname = models.CharField(max_length=50)
    pphone = models.CharField(max_length=50)
    bg = models.CharField(max_length=50)
    reqdate = models.DateField()
    did = models.IntegerField()
    dname = models.CharField(max_length=50)
    dphone = models.CharField(max_length=20)
    msg = models.CharField(max_length=150)
    status = models.CharField(max_length=20, default='New Request')

# ----------------------
# Direct Request model
# ----------------------
class directrequest(models.Model):
    reqno = models.IntegerField()
    pid = models.IntegerField()
    pname = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    bg = models.CharField(max_length=50)
    rdate = models.DateField()
    details = models.CharField(max_length=150)
    nofb = models.IntegerField()
    status = models.CharField(max_length=25, default='New Request')

# ----------------------
# Feedback model
# ----------------------
class feedback(models.Model):
    pid = models.IntegerField()
    pname = models.CharField(max_length=50)
    did = models.IntegerField()
    msg = models.CharField(max_length=150)

# ----------------------
# Notification model
# ----------------------
class notification(models.Model):
    venue = models.CharField(max_length=100)
    purpose = models.CharField(max_length=100)
    pdate = models.DateField()
    ptime = models.CharField(max_length=50)
    note = models.CharField(max_length=250)