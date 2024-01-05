from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
import re
from userreg.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

# Create your views here.

def reg(request):
    a = register.objects.all()
    if request.method == 'POST':
        username  = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        # Define a regular expression pattern for the password constraints
        password_pattern = r'^(?=.*[A-Z])(?=.*[\W_]).{8,}$'

        if password == cpassword:
            # Check if the password meets the required constraints
            if re.match(password_pattern, password):
                for i in a:
                    if i.username == username:
                        return HttpResponse('Username already taken')
                    elif i.email == email:
                        return HttpResponse('Email already taken')
                else:
                    b = register(username=username, email=email, password=password)
                    b.save()
                    subject = f"Thank you {username}!"
                    message = f"Your account is created an dyou can login with your credentials"

                    email_from = EMAIL_HOST_USER
                    send_mail(subject, message, email_from, ['nivedsankarpm7@gmail.com'])
                    return redirect(login)
            else:
                return HttpResponse("Password must be at least 8 characters long, including at least one special character and one capital letter")
        else:
            return HttpResponse("Passwords didn't match")

    return render(request, 'reg.html')

def login(request):
    a = register.objects.all()
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        for i in a:
            if i.email == email and i.password == password:
                return HttpResponse('Login successfull')
        else:
            return HttpResponse('Login failed')
    return render(request,'login.html')
