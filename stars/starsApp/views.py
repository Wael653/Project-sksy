from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.forms.models import model_to_dict
from .forms import UserForm, ProfileForm, PasswordForm, ReservationForm
from .models import Contact, Reservation, Workplace




from django.views.generic import FormView, TemplateView
from .forms import ContactForm
from django.urls import reverse_lazy


# Create your views here.
def index(request):
    context = {'workplaces' : Workplace.objects.all()}
    return render(request, 'index.html', context)


def imprint(request):
    return render(request, 'impressum.html')


def user(request):
    return render(request, 'nutzer.html', {'current_user': request.user})


def reservations(request):
    if request.user.id is not None:
        workplace = Workplace.objects.all()
        reservation = Reservation.objects.all().filter(user=request.user)
        return render(request, 'reservierungen.html', {'reservations': reservation, 'workplaces': workplace})
    else:
        return render(request, 'reservierungen.html')


def reservieren(request):
    form = ReservationForm(request.POST or None, initial={'user': request.user})
    if form.is_valid():
        form.save()
        return redirect('reservations')
    else:
        return render(request, 'reservieren.html', {'form': form})


#def support(request):
     #if request.method == "POST":
      #      contact = Contact()
       #     contact.name = request.POST['name']
         #   contact.subject = request.POST['subject']
        #    from_email= request.POST['email']
          #  message = request.POST['message']
          #  contact.save()
           # return HttpResponse("<h1 style = font-family:Verdana> Thanks, your message was successfully submitted.</h1>")
     #else:
      #  return render(request, 'support.html')


def support(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send()
            return HttpResponse("<h1> Die Anfrage wurde erfolgreich versendet!</h1>")
    else:
        form = ContactForm()
    return render(request, 'support.html', {'form': form})

def arbeitsplaetze(request):
    context = {'workplaces' : Workplace.objects.all()}
    return render(request, 'arbeitsplaetze.html', context)


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
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


def delete_User(request, nutzername):
    user = User.objects.get(username = nutzername)
    user.delete()
    return redirect('index')

