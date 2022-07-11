
from datetime import date, datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from .forms import UserForm, ProfileForm, PasswordForm, LoginForm, ContactForm
from .models import Reservation, Workplace, Review
from django.contrib import messages
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy, reverse


# Create your views here.
def index(request):
    context = {'workplaces' : Workplace.objects.all()}
    return render(request, 'index.html', context)


def imprint(request):
    return render(request, 'impressum.html')


def user(request):
    return render(request, 'nutzer.html', {'current_user': request.user})

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

def timeslots(request, wp_id):
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
    wp1 = Workplace.objects.get(id = wp_id)

    for wp_res in wp1.reservation_set.all():
        times.remove(wp_res.time)

    return render(request, 'reservieren.html', {'wp': wp1, 'slots_times': slots_times, 'set_res': times})


def reserve(request, time_slot, wp_id):
    wp1 = Workplace.objects.get(id=wp_id)
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
    context = {'workplaces' : Workplace.objects.all()}
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

        current_time = datetime.now().strftime("%H")
        key_time = int(current_time) - 7
        if len(reservierungen) == 0:
            messages.error(request, f'Du kannst den Arbeitsplaz {workplace} nicht bewerten, denn du hast diesen noch nicht reserviert.')
            return HttpResponseRedirect(reverse('wp-rate', args = [workplace.id]))
        
        f = list(filter(lambda r: r.date < date.today(), reservierungen))  
        r = min(reservierungen, key=lambda x:x.time)
        if len(f) == 0 and key_time <= r.time:
            messages.info(request, f'Du kannst deinen reservierten Arbeitsplatz aktuell nicht bewerten, denn das Ende deiner Reservierung ist noch nicht um {reservation_end(time = r.time)}:00 Uhr erreicht.')
            return HttpResponseRedirect(reverse('wp-rate', args = [workplace.id]))

        Review(user = user, wp = workplace, text = comment, rate = rate).save()
        messages.success(request, ("Vielen Dank für dein Feedback!"))
        return HttpResponseRedirect(reverse('wp-rate', args = [wp_id]))         

     else:
        return render(request, 'rating.html', context)
