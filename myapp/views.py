from django.shortcuts import render, redirect
from myapp.models import doner, patient, stock, directrequest, bloodrequest, feedback, notification
from datetime import date, timedelta, datetime
from django.db.models.functions import Coalesce
from django.db.models import Sum, Max, Value, F
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError

# Create your views here.

def index(request):
    cdate = date.today()
    drec = doner.objects.filter(status='Inactive')
    for j in drec:
        ldate = j.ldate
        id = j.id
        date_format = "%Y-%m-%d"
        a = datetime.strptime(str(ldate), date_format)
        b = datetime.strptime(str(cdate), date_format)
        delta = b - a
        diff = int(delta.days)
        if diff > 180:
            doner.objects.filter(id=id).update(status='Active')
    drec = doner.objects.filter(status='Active')
    ap = an = bp = bn = abp = abn = op = on = 0

    brec = stock.objects.filter(bgroup='A+')
    if brec.exists():
        for j in brec:
            ap = j.qty
    brec = stock.objects.filter(bgroup='A-')
    if brec.exists():
        for j in brec:
            an = j.qty
    brec = stock.objects.filter(bgroup='B+')
    if brec.exists():
        for j in brec:
            bp = j.qty
    brec = stock.objects.filter(bgroup='B-')
    if brec.exists():
        for j in brec:
            bn = j.qty
    brec = stock.objects.filter(bgroup='AB+')
    if brec.exists():
        for j in brec:
            abp = j.qty
    brec = stock.objects.filter(bgroup='AB-')
    if brec.exists():
        for j in brec:
            abn = j.qty
    brec = stock.objects.filter(bgroup='O+')
    if brec.exists():
        for j in brec:
            op = j.qty
    brec = stock.objects.filter(bgroup='O-')
    if brec.exists():
        for j in brec:
            on = j.qty
    return render(request, "index.html",
                  {"drec": drec, "ap": ap, "an": an, "bp": bp, "bn": bn, "abp": abp, "abn": abn, "op": op, "on": on})



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import doner  # Adjust model name if different
from datetime import datetime

def donerreg(request):
    if request.method == 'POST':
        try:
            fname = request.POST.get('t1')
            lname = request.POST.get('t2')
            address = request.POST.get('t3')
            district = request.POST.get('t4')
            city = request.POST.get('t5')
            phone = request.POST.get('t6')
            email = request.POST.get('t7')
            age = request.POST.get('t8')
            gender = request.POST.get('t9')
            bgroup = request.POST.get('t10')
            ldate = request.POST.get('t11')
            allergy = request.POST.get('t12')
            disease = request.POST.get('t13')
            username = request.POST.get('t14')
            password = request.POST.get('t15')

            # Handle uploaded photo file (optional)
            photo = request.FILES.get('file')  # Won't raise KeyError

            if not photo:
                messages.error(request, "Photo upload is required.")
                return redirect('donerreg')  # Replace with actual template name

            # Create Donor object and save
            donor = doner(
                fname=fname,
                lname=lname,
                address=address,
                district=district,
                city=city,
                phone=phone,
                email=email,
                age=age,
                gender=gender,
                bgroup=bgroup,
                ldate=ldate,
                allergy=allergy,
                disease=disease,
                photo=photo,
                username=username,
                password=password  # Consider hashing this if you're not using Django's auth system
            )
            donor.save()

            messages.success(request, "Registration successful! Please wait for admin approval.")
            return redirect('donerreg')  # Or redirect to login page

        except Exception as e:
            print("Error in donor registration:", str(e))  # For debugging
            messages.error(request, "Something went wrong. Please try again.")
            return redirect('donerreg')
    
    return render(request, 'onlinedonerreg.html')  # Adjust template name

def patient_registration(request):
    error_message = ''  # Initialize error_message

    if request.method == "POST":
        fname = request.POST.get('fn')
        lname = request.POST.get('ln')
        phone = request.POST.get('ph')
        email = request.POST.get('em')
        uname = request.POST.get('un')
        pword = request.POST.get('pw')
        
        try:
            # Save patient registration details
            sa = patient(fname=fname, lname=lname, phone=phone, email=email, uname=uname, pword=pword)
            sa.save()
            
            registered_fname = fname
            # Send registration success email
            send_registration_email(email, registered_fname, 'patient')

            
            return redirect("/h/")  # Redirect to home page after successful registration
        except IntegrityError:
            # Handle the case where the username is not unique
            error_message = 'Username already exists. Please choose a different username.'
    
    # Pass error_message to the template context
    return render(request, "onlinepatientreg.html", {'error_message': error_message})

# Define function to send registration email
def send_registration_email(email, registered_fname, registration_type):
    subject = 'Registration Successful'
    if registration_type == 'patient':
        message = f'Thank you for registering as a patient, {registered_fname}!'
    elif registration_type == 'donor':
        message = f'Thank you for registering as a donor and being a future lifesaver, {registered_fname}!'
    else:
        message = 'Thank you for registering!'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def loginpage(request):
    if request.method == "POST":
        u = request.POST.get('t1')
        p = request.POST.get('t2')
        found = 0
        srec = doner.objects.filter(uname=u, pword=p)
        if srec.exists():
            found = 1
            for j in srec:
                id = j.id
                n = j.fname
                ph = j.phone
                r = j.rights

        if found == 0:
            srec = patient.objects.filter(uname=u, pword=p)
            if srec.exists():
                found = 1
                for j in srec:
                    id = j.id
                    n = j.fname
                    ph = j.phone
                    r = j.rights

        if found == 0:
            msg = "Sorry, Invalid user"
        else:
            request.session['id'] = id
            request.session['name'] = n
            request.session['phone'] = ph
            request.session['uname'] = u
            request.session['pword'] = p
            request.session['rights'] = r
            if r == "admin":
                return redirect("/ap/")
            elif r == "user":
                return redirect("/pp/")
            elif r == "Doner":
                return redirect("/dp/")
            elif r == "New Doner":
                msg = "You are not approved"
            else:
                msg = "Sorry, your application was rejected"
                return render(request, "loginpage.html", {"show_popup": msg})

    return render(request, "loginpage.html")


def adminpage(request):
    drec = doner.objects.filter(status='Active', rights='Doner')
    return render(request, "AdminPage.html", {"drec": drec})


def patientpage(request):
    drec = doner.objects.filter(status='Active', rights='Doner')
    ap = an = bp = bn = abp = abn = op = on = 0

    brec = stock.objects.filter(bgroup='A+')
    if brec.exists():
        for j in brec:
            ap = j.qty
    brec = stock.objects.filter(bgroup='A-')
    if brec.exists():
        for j in brec:
            an = j.qty
    brec = stock.objects.filter(bgroup='B+')
    if brec.exists():
        for j in brec:
            bp = j.qty
    brec = stock.objects.filter(bgroup='B-')
    if brec.exists():
        for j in brec:
            bn = j.qty
    brec = stock.objects.filter(bgroup='AB+')
    if brec.exists():
        for j in brec:
            abp = j.qty
    brec = stock.objects.filter(bgroup='AB-')
    if brec.exists():
        for j in brec:
            abn = j.qty
    brec = stock.objects.filter(bgroup='O+')
    if brec.exists():
        for j in brec:
            op = j.qty
    brec = stock.objects.filter(bgroup='O-')
    if brec.exists():
        for j in brec:
            on = j.qty
    return render(request, "PatientPage.html", {"drec": drec, "ap": ap, "an": an, "bp": bp, "bn": bn, "abp": abp, "abn": abn, "op": op, "on": on})


def patientdirectrequest(request):
    pid = request.session['id']
    pname = request.session['name']
    ppho = request.session['phone']
    brec = stock.objects.all()
    if request.method == "POST":
        bg = request.POST.get('s1')
        nob = request.POST.get('s2')
        rdate = request.POST.get('t6')
        ms = request.POST.get('t7')
        max_reqno = directrequest.objects.aggregate(max_reqno=Coalesce(Max('reqno'), Value(0)))['max_reqno']
        mbno = int(max_reqno) + 1
        da = directrequest(reqno=mbno, pid=pid, pname=pname, phone=ppho, bg=bg, rdate=rdate, details=ms, nofb=nob)
        da.save()
        return redirect("/pp/")
    return render(request, "PatientDirectRequest.html", {"pname": pname, "ppho": ppho, "brec": brec})


def patientrequest(request, id):
    cdate = date.today()

    if request.method == "POST":
        pid = request.session['id']
        pname = request.session['name']
        ppho = request.session['phone']
        drec = doner.objects.filter(id=id)
        for j in drec:
            bg = j.bgroup
            did = j.id
            dname = j.fname
            dph = j.phone
        max_reqno = bloodrequest.objects.aggregate(max_reqno=Coalesce(Max('reqno'), Value(0)))['max_reqno']
        mbno = int(max_reqno) + 1
        rdate = request.POST['t6']
        msg = request.POST.get('t10')
        sa = bloodrequest(reqno=mbno, rdate=cdate, pid=pid, pname=pname, pphone=ppho, bg=bg, reqdate=rdate, did=did,
                          dname=dname, dphone=dph, msg=msg)
        sa.save()

        subject = 'You got a blood request!'
        message = f'Dear {dname},\n\nA patient named {pname} has requested blood. Here are the details:\n\n\nPatient Phone Number: {ppho}\nBlood Group: {bg}\nRequired Date: {rdate}\nMessage: {msg}\n\nPlease respond accordingly.\n\nBest regards,\nThe Blood Donation Team'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [j.email]
        send_mail(subject, message, from_email, recipient_list)

        return redirect("/pp/")

    # Fetch patient details from the database
    patient = doner.objects.get(id=id)

    # Pass patient details to the template context
    context = {
        "cdate": cdate,
        "pid": patient.id,
        "pname": patient.fname,
        "ppho": patient.phone,
        "bg": patient.bgroup,
        "did": patient.id,
        "dname": patient.fname,
        "dph": patient.phone,
    }

    return render(request, "PatientRequestPage.html", context)


def userviewstatus(request):
    prec = bloodrequest.objects.filter(pid=request.session['id'])
    return render(request, "PatientViewStatus.html", {"prec": prec})


def donerpage(request):
    name = request.session['name']
    return render(request, "DonerPage.html", {"name": name})


def donerpatientapproval(request):
    prec = bloodrequest.objects.filter(did=request.session['id'], status='New Request')
    return render(request, "DonerPatientApproval.html", {"prec": prec})


def donerpatientapp(request, id):
    if request.method == 'GET':
        # Retrieve the blood request object using the provided id
        blood_request = bloodrequest.objects.get(id=id)
        
        # Update the status of the blood request
        blood_request.status = 'Accepted'
        blood_request.save()

        # Send an email to the patient
        send_email_to_patient(blood_request)
        
        return redirect('/dp/')  # Redirect to the previous page
        
def send_email_to_patient(blood_request):
    # Retrieve the patient associated with the blood request
    patient_obj = patient.objects.get(fname=blood_request.pname)
    
    # Retrieve the patient's email address
    patient_email = patient_obj.email
    
    # Compose your email message here
    subject = 'Your Blood Donation Request Has Been Accepted'
    message = f'''
    Dear {blood_request.pname},
    
    Your blood donation request has been accepted. 
    Please Keep in touch with {blood_request.dname}
    Phone:{blood_request.dphone}
    
   
    
    Best regards,
    Blood Bank X
    '''

    sender_email = 'abloodbank9@gmail.com'  # Update with your sender email address
    
    # Send the email
    send_mail(subject, message, sender_email, [patient_email])


def donerpatientreject(request, id):
    blood_request = bloodrequest.objects.get(id=id)  # Assuming BloodRequests is your model
    # Retrieve the patient using the Patient model
    patient_instance = patient.objects.get(fname=blood_request.pname)

    # Update the status of the blood request
    blood_request.status = 'Rejected'
    blood_request.save()

    # Send email notification to the patient
    subject = 'Blood Request Rejected'
    message = 'Your blood request has been rejected. We apologize for the inconvenience.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [patient_instance.email]  # Assuming email field exists in Patient model

    # Send the email
    send_mail(subject, message, from_email, recipient_list)

    return redirect("/dp/")


def viewdonerhistory(request):
    drec = bloodrequest.objects.filter(did=request.session['id'])
    return render(request, "DonerViewHistory.html", {"drec": drec})


def viewdonernotification(request):
    nrec = notification.objects.all()
    return render(request, "ViewNotification1.html", {"nrec": nrec})


def viewdonerfeedback(request):
    frec = feedback.objects.filter(did=request.session['id'])
    return render(request, "DonerViewFeedback.html", {"frec": frec})


def admindonerapproval(request):
    drec = doner.objects.filter(rights='New Doner')
    return render(request, "AdminDonerApproval.html", {"drec": drec})


def approvedoner(request, id):
    doner.objects.filter(id=id).update(rights='Doner')
    return redirect("/adapr/")


def rejectdoner(request, id):
    doner.objects.filter(id=id).update(rights='reject')
    return redirect("/adapr/")


def adminviewhistory(request, id):
    drec = bloodrequest.objects.filter(did=id)
    return render(request, "AdminDonerHistory.html", {"drec": drec})


def adminnotification(request):
    if request.method == "POST":
        venue = request.POST.get('t1')
        purpose = request.POST.get('t2')
        pdate = request.POST.get('t3')
        ptime = request.POST.get('t4')
        note = request.POST.get('t5')
        sa = notification(venue=venue, purpose=purpose, pdate=pdate, ptime=ptime, note=note)
        sa.save()
        return redirect("/ap/")
    return render(request, "AdminNotification.html")


def changepass(request):
    if request.method == "POST":
        a = request.POST.get('t1')
        b = request.POST.get('t2')
        c = request.POST.get('t3')
        u = request.session['uname']
        p = request.session['pword']
        r = request.session['rights']
        if p == a:
            if b == c:
                if r == 'Doner':
                    doner.objects.filter(uname=u, pword=p).update(pword=b)
                else:
                    patient.objects.filter(uname=u, pword=p).update(pword=b)
                return redirect('/log/')
            else:
                msg = "Sorry, password mismatch"
        else:
            msg = "Invalid user"
    return render(request, "Changepassword.html")


def patientnotification(request):
    nrec = notification.objects.all()
    return render(request, "ViewNotification.html", {"nrec": nrec})


def patientfeedback(request):
    prec = bloodrequest.objects.filter(pid=request.session['id'], status='Transfered')
    return render(request, "PatientFeedback1.html", {"prec": prec})


def patientfeedback1(request, did):
    if request.method == "POST":
        ms = request.POST.get('m')
        sa = feedback(pid=request.session['id'], pname=request.session['name'], did=did, msg=ms)
        sa.save()
        return redirect("/pp/")
    name = request.session['name']
    return render(request, "PatientFeedback.html", {"name": name})


def adminbloodtransfer(request):
    prec = bloodrequest.objects.all()  # Fetch all blood requests
    return render(request, "AdminBloodTransfer.html", {"prec": prec})


def admintransfer(request, id):
    # Update the blood request status to 'Transfered'
    bloodrequest.objects.filter(id=id).update(status='Transfered')
    
    # Update donor status to 'Inactive' and last donation date to today's date
    blood_req = bloodrequest.objects.get(id=id)
    donor_id = blood_req.did_id
    doner.objects.filter(id=donor_id).update(ldate=date.today(), status='Inactive')
    
    return redirect("/abt/")  # Redirect to the blood transfer page


def adminblooddirecttransfer(request):
    # Fetch all direct requests excluding transferred ones
    brec = directrequest.objects.exclude(status='Transfered')
    return render(request, "AdminDirectTransfer.html", {"brec": brec})


def admindirecttrans(request, id):
    if request.method == 'GET':
        # Retrieve the direct request object using the provided id
        direct_request = directrequest.objects.get(id=id)
        # Retrieve the patient details associated with the direct request
        patient_info = patient.objects.get(id=direct_request.pid)
        
        # Send email to the patient
        subject = 'Blood Request Approved'
        message = f"Dear {patient_info.fname},\n\nYour blood unit(s) request has been approved .\n\nPlease visit Blood Bank X for collecting blood units:\n\n https://maps.app.goo.gl/7bs1TWxn2R9ewmvA9\n\nBest regards,\n[Blood Bank X]"
        sender_email = 'abloodbank9@gmail.com'  # Replace with your sender email address
        recipient_email = [patient_info.email]  # Assuming you have the patient's email
        
        # Send the email
        send_mail(subject, message, sender_email, recipient_email)
        
        # Update the direct request status to 'Transfered'
        direct_request.status = 'Transfered'
        direct_request.save()
        
        # Update stock quantity
        bg = direct_request.bg
        no = direct_request.nofb
        stock.objects.filter(bgroup=bg).update(qty=F('qty') - no)
        
        return redirect("/abdt/")  # Redirect to the direct blood transfer page


def reject_request(request, id):
    # Retrieve the direct request
    direct_request = directrequest.objects.get(id=id)
    # Retrieve the patient details associated with the direct request
    patient_info = patient.objects.get(id=direct_request.pid)
    
    # Send email to the patient
    subject = 'Blood Transfer Rejected'
    message = f"Dear {patient_info.fname},\n\nWe regret to inform you that your blood transfer request has been rejected.\n\nPlease Contact Us for further details\n\nBest regards,\n[Blood Bank X]"
    sender_email = 'abloodbank9@gmail.com'  # Replace with your sender email address
    recipient_email = [patient_info.email]  # Assuming you have the patient's email
    
    # Send the email
    send_mail(subject, message, sender_email, recipient_email)
    
    # Delete the direct request
    direct_request.delete()
    
    return redirect("/abdt/")  # Redirect back to the direct blood transfer page


def adminstock(request):
    if request.method == "POST":
        bg = request.POST.get('t1')
        qt = request.POST.get('t2')
        brec = stock.objects.filter(bgroup=bg)
        if brec.exists():
            stock.objects.filter(bgroup=bg).update(qty=F('qty') + qt)
        else:
            sa = stock(bgroup=bg, qty=qt)
            sa.save()
    brec = stock.objects.all()
    return render(request, "Adminstock.html", {"brec": brec})


def load_options(request):
    selected_value = request.GET.get('selected_value')
    # Perform any necessary data retrieval or processing based on the selected value
    options = []
#   options = ['Option 3.1', 'Option 3.2', 'Option 3.3']

    wrd = stock.objects.filter(bgroup=selected_value)
    for j in wrd:
        qty = j.qty
    print(qty)
    for j in range(1, qty + 1):
        options.append(j)

    data = {
        'options': options,
    }

    return JsonResponse(data)


def delnotification(request, id):
    notification.objects.filter(id=id).delete()
    return redirect("/uvnot/")