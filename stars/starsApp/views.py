from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.forms.models import model_to_dict
from .forms import UserForm, ProfileForm, PasswordForm
from .models import Contact, Workplace


# Create your views here.
def index(request):
    return render(request, 'index.html')

def imprint(request):
    return render(request, 'impressum.html')

def user(request):
    return render(request, 'nutzer.html', {'current_user': request.user})

def reservations(request):
    return render(request, 'reservierungen.html')

def support(request):
     if request.method == "POST":
            contact = Contact()
            contact.name = request.POST['name']
            contact.subject = request.POST['subject']
            from_email= request.POST['email']
            message = request.POST['message']
            contact.save()
            return HttpResponse("<h1 style = font-family:Verdana> Thanks, your message was successfully submitted.</h1>")
     else:
        return render(request, 'support.html')
    
def arbeitsplaetze(request):
    context = {'workplaces' : Workplace.objects.all()}
    return render(request, 'arbeitsplaetze.html', context)

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'registrieren.html', {'form': form})

def login(request):
    return render(request, 'login.html')

def logout(request):
    return render(request, 'logout.html')

def change_profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('user')
    else:
        return render(request, 'setting_profile.html', {'form': form})

def change_password(request):
    form = PasswordForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('user')
    else:
        return render(request, 'setting_password.html', {'form': form})
