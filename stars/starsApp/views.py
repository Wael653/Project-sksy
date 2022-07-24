from datetime import date, datetime
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse
from django.forms.models import model_to_dict
from .forms import UserForm, ProfileForm, PasswordForm, LoginForm, ContactForm
from .models import Reservation, Workplace, Unit, Room, Review, ProfileUser
from django.http import HttpResponse, Http404, JsonResponse
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from .forms import UserForm, ProfileForm, PasswordForm, LoginForm, ContactForm, DateForm
from .models import Reservation, Workplace, Unit, Room, WorkplaceDevice
from django.conf import settings
from django.contrib import messages
from django.views.generic import FormView, TemplateView
from django.urls import reverse
from django .contrib.auth.decorators import login_required 
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMessage

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
    date_form = DateForm()
    selected_date = date.today()
    if request.GET:
        selected_date = request.GET['date']
        date_split = selected_date.split("-")
        selected_date = datetime.date(int(date_split[0]), int(date_split[1]), int(date_split[2]))

    times = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14}
    wp1 = Workplace.objects.get(nummer=wp_nr)
    times2 = {0}

    for wp_res in wp1.reservation_set.all().filter(date=selected_date):
        times2.add(wp_res.time)

    return render(request, 'reservieren.html', {'wp': wp1, 'slots_times': slots_times,
                                                'times': times-times2, 'sunday': selected_date.weekday(),
                                                'selected_date': selected_date, 'date_form': date_form})


def reserve(request, time_slot, wp_nr, datum):
    wp1 = Workplace.objects.get(nummer=wp_nr)
    res1 = wp1.reservation_set.create(user=request.user, date=datum, time=time_slot)
    name = request.user.first_name
    subject = 'Bestätigung deiner Rservierung'
    msg = render_to_string('email_support.html', {'name': name , 'wp_nummer': wp1.nummer, 'raum_nummer': wp1.raum, 'datum': res1.date, 'wp':wp1, 'timeslote': get_timeslot(res1.time) }) 
    plain_msg = msg.replace("\r\n", "<br>")
    plain_msg = strip_tags(msg)
    msg_object = EmailMessage (
        subject = subject,
        body = plain_msg,
        from_email = "Stars <stars@example.com>",
        to = [request.user.email]
    )
    file = open("stars-logo-01.png", "rb")
    msg_object.attach('stars-logo-01.png', file.read(), 'image/png')
    msg_object.send()
    messages.info(request, ("Vielen Dank, wir haben dir eine Bestätigungsemail für deine Reservierung geschickt."))
    return redirect('reservations')


def delete_reserve(request, r_id):
    Reservation.objects.get(pk=r_id).delete()
    return redirect('reservations')

def reservation_end(time):
    if time == 1: return 9
    elif time == 2: return 10
    elif time == 3: return 11
    elif time == 4: return 12
    elif time == 5: return 13
    elif time == 6: return 14
    elif time == 7: return 15
    elif time == 8: return 16
    elif time == 9: return 17
    elif time == 10: return 18
    elif time == 11: return 19
    elif time == 12: return 20
    elif time == 13: return 21
    else: return 22


def get_timeslot(time):
    if time == 1: return "8:00-9:00"
    elif time == 2: return "9:00-10:00"
    elif time == 3: return "10:00-11:00"
    elif time == 4: return "11:00-12:00"
    elif time == 5: return "12:00-13:00"
    elif time == 6: return "13:00-14:00"
    elif time == 7: return "14:00-15:00"
    elif time == 8: return "15:00-16:00"
    elif time == 9: return "16:00-17:00"
    elif time == 10: return "17:00-18:00"
    elif time == 11: return "18:00-19:00"
    elif time == 12: return "19:00-20:00"
    elif time == 13: return "20:00-21:00"
    else: return "21:00-22:00"



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
            cur_user = request.user
            ProfileUser.objects.get_or_create(user = cur_user, username = cur_user.username, first_name = cur_user.first_name, last_name = cur_user.last_name, email = cur_user.email)
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
 p_user = request.user.profile_user  
 form = ProfileForm(instance = p_user)
 if request.method == 'POST':    
    form = ProfileForm(request.POST, request.FILES, instance = p_user)
    if form.is_valid(): 
        form.save()
        request.user.first_name = form.cleaned_data['first_name']
        request.user.last_name = form.cleaned_data['last_name']
        request.user.username = form.cleaned_data['username']
        request.user.email = form.cleaned_data['email']
        request.user.save()
        return redirect ('user')

 else:
    return render(request, 'setting_profile.html', {'form': form})

def delete_User(request, nutzername):
    user = User.objects.get(username = nutzername)
    user.delete()
    return redirect('index')



def change_password(request):
    form = PasswordForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('user')
    else:
        return render(request, 'setting_password.html', {'form': form})


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


@login_required(login_url= 'login')
def rating(request, wp_id):
     workplace = Workplace.objects.get(pk = wp_id)
     reservierungen = Reservation.objects.all().filter(user = request.user, wp = workplace)
     previous_reviews = Review.objects.filter( wp = workplace) 
     user = request.user
     context = {'wp': workplace, 'previous_reviews': previous_reviews}
       
     if request.method == 'POST':
        rate = request.POST.get('rating')    
        comment = request.POST.get('comment')
        if rate is None:
           messages.warning(request, ("Keine Option wurde ausgewählt!"))
           return HttpResponseRedirect(reverse('wp-rate', args = [workplace.id]))

        if len(reservierungen) == 0:
            messages.error(request, f'Du kannst den Arbeitsplaz {workplace} nicht bewerten, denn du hast diesen noch nicht reserviert.')
            return HttpResponseRedirect(reverse('wp-rate', args = [workplace.id]))
        

        first_reservation = reservierungen.first()
        current_time = datetime.datetime.now().strftime("%H")
        current_time = int(current_time) -7
        current_time = max(0, current_time)

        if date.today() < first_reservation.date or (date.today == first_reservation.date and current_time <= first_reservation.time):
            messages.info(request, f'Du kannst deinen reservierten Arbeitsplatz aktuell nicht bewerten, denn das Ende deiner Reservierung am {first_reservation.date} um {reservation_end(time = first_reservation.time)}:00 Uhr ist noch nicht eingetroffen.')
            return HttpResponseRedirect(reverse('wp-rate', args = [workplace.id]))
       
     #   Review(user = user, wp = workplace, text = comment, rate = rate).save()
        messages.success(request, ("Vielen Dank für dein Feedback!"))
        return HttpResponseRedirect(reverse('wp-rate', args = [wp_id]))         

     else:
        return render(request, 'rating.html', context)

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

    
