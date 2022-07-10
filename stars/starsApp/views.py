from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.forms.models import model_to_dict
from .forms import UserForm, ProfileForm, PasswordForm, ReservationForm, LoginForm, ContactForm
from .models import Reservation, Workplace, Unit, Room
from django.contrib import messages
from django.views.generic import FormView, TemplateView
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

def support(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send()
            return render(request, 'message_support.html')
            
    else:
        form = ContactForm()
    return render(request, 'support.html', {'form': form})

def arbeitsplaetze(request):
    context = {'workplaces' : Workplace.objects.all(), 'units' : Unit.objects.all(), 'rooms': Room.objects.all()}
    return render(request, 'arbeitsplaetze.html', context)


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, ("Nutzer wurde erfolgreich erstellet. Bitte logge dich ein!"))
            return redirect('login') 
        else:
            {'form': form}
    else:
        form = UserForm()
    return render(request, 'registrieren.html', {'form': form})


def login_user(request):
    if request.method == "POST": 
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('user')
        else:   
            messages.error(request, ("Einloggen fehlgeschlagen, ungültiger Benutzername oder Passwort."))
            return redirect('login')
    else:
        form = LoginForm()       
        return render(request, 'registration/login.html', {'form': form})


def logout_user(request):
        logout(request)
        messages.success(request, ("Du bist ausgeloggt"))
        return redirect('login')   


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

def get_rooms_ajax(request):
    if request.method == "POST":
        print("Testlog")
        unit_id = request.POST['unit_id']
        try:
            unit = Unit.objects.filter(id = unit_id).first()
            rooms = Room.objects.filter(unit = unit)
        except Exception:
            raise Http404("Fehler beim Laden der Räume")
        return JsonResponse(list(rooms.values('id', 'nummer')), safe = False) 
