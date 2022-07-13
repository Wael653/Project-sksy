
from datetime import date


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.forms.models import model_to_dict


from .forms import UserForm, ProfileForm, PasswordForm, LoginForm, ContactForm
from .models import Reservation, Workplace, Unit, Room, WorkplaceDevice

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
        slots = {
            1: '8:00-9:00',
            2: '9:00-10:00',
            3: '10:00-11:00',
            4: '11:00-12:00',
            5: '12:00-13:00',
            6: '13:00-14:00',
            7: '14:00-15:00',
            8: '15:00-16:00',
            9: '16:00-17:00',
            10: '17:00-18:00',
            11: '18:00-19:00',
            12: '19:00-20:00',
            13: '20:00-21:00',
            14: '21:00-22:00'
        }
        workplace = Workplace.objects.all()
        user_reservation = Reservation.objects.all().filter(user=request.user)
        return render(request, 'reservierungen.html', {'reservations': user_reservation, 'workplaces': workplace,
                                                       'slots': slots})
    else:
        return render(request, 'reservierungen.html')

def timeslots(request, wp_nr):
    slots_times = {
        1: '8:00-9:00',
        2: '9:00-10:00',
        3: '10:00-11:00',
        4: '11:00-12:00',
        5: '12:00-13:00',
        6: '13:00-14:00',
        7: '14:00-15:00',
        8: '15:00-16:00',
        9: '16:00-17:00',
        10: '17:00-18:00',
        11: '18:00-19:00',
        12: '19:00-20:00',
        13: '20:00-21:00',
        14: '21:00-22:00'
    }
    times = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14}
    wp1 = Workplace.objects.get(nummer=wp_nr)

    for wp_res in wp1.reservation_set.all():
        times.remove(wp_res.time)

    return render(request, 'reservieren.html', {'wp': wp1, 'slots_times': slots_times, 'set_res': times})


def reserve(request, time_slot, wp_nr):
    wp1 = Workplace.objects.get(nummer=wp_nr)
    wp1.reservation_set.create(user=request.user, date=date.today(), time=time_slot)
    return redirect('reservations')


def delete_reserve(request, r_id):
    Reservation.objects.get(pk=r_id).delete()
    return redirect('reservations')



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
        unit_id = request.POST['unit_id']
        try:
            unit = Unit.objects.filter(id = unit_id).first()
            rooms = Room.objects.filter(unit = unit)
        except Exception:
            #TODO: Richtige Fehlermeldung ausgeben
            raise Http404("Fehler beim Laden der Räume")
        return JsonResponse(list(rooms.values('id', 'nummer')), safe = False) 

def get_workplaces_ajax(request):
    if request.method == "POST":
        room_id = request.POST['room_id']
        try:
            room = Room.objects.filter(id = room_id).first()
            workplaces = Workplace.objects.filter(raum = room)
        except Exception:
            #TODO: Richtige Fehlermeldung ausgeben
            raise Http404("Fehler beim Laden der Arbeitsplätze")
        return JsonResponse(list(workplaces.values('id', 'nummer')), safe = False) 

def get_filteroptions_ajax(request):
    if request.method == "POST":
        room_id = request.POST['room_id']
        try:
            room = Room.objects.filter(id = room_id).first()
            workplaces = Workplace.objects.filter(raum = room)
            workplaceDevices = WorkplaceDevice.objects.none()
            for workplace in workplaces:
                workplaceDevices = workplaceDevices | workplace.geraete.all()
        except Exception:
            print(Exception)
            raise HttpResponse(status=500)
        return JsonResponse(list(workplaceDevices.distinct().values('id', 'bezeichnung')), safe = False) 

def get_filtered_workplaces_ajax(request):
    if request.method == "POST":
        room_id = request.POST['room_id']
        device_id = request.POST['device_id']
        try:
            room = Room.objects.filter(id = room_id).first()
            workplaces = Workplace.objects.filter(raum = room, geraete__id = device_id)
        except Exception:
            #TODO: Richtige Fehlermeldung ausgeben
            raise Http404("Fehler beim Laden der Arbeitsplätze")
        return JsonResponse(list(workplaces.values('id', 'nummer')), safe = False) 