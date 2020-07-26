from django.shortcuts import render
from .forms import AccountsForm, loginForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse
from Management.models import Customer
# Create your views here.


def Registration(request):
    form = AccountsForm(request.POST or None)
    context = {"form": form}
    template = "Registration.html"

    if form.is_valid():
        checkingForm = form.save(commit=False)
        # print(checkingForm.Email)
        # print(checkingForm.UserName)
        checkingForm.save()
        return HttpResponseRedirect('/login/')

    return render(request, template, context)


def loginUser(request):
    loginF = loginForm(request.POST or None)
    template = "Login.html"
    context = {'login': loginF}
    if request.method == "POST":
        Email = request.POST.get('Email')
        # print(Email)
        Password = request.POST.get('password')
        check = request.POST.get('check')
        # print(Password)
        print(check)
        auth = authenticate(request, username=Email, password=Password)
        if auth == None:
            errormessage = "Please Check Username or password is valid"
            context['error'] = errormessage
            print(auth)
        else:
            login(request, auth)
            try:
                Customer.objects.create(
                    Profile=request.user, name=request.user.UserName) #creating the objects to the onetonefield to the Customer model for the further info about customers
                # messages.success(request, 'Yeah')
            except:
                pass
            if(check):
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponseRedirect(reverse('Main'))
    return render(request, template, context)


def Unauth(request):
    template = "Unauth.html"
    return render(request, template)
