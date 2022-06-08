from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.forms.models import model_to_dict
from .models import Workplace

# Create your views here.
def index(request):
    return render(request, 'index.html')

def imprint(request):
    return render(request, 'impressum.html')

def user(request):
    return render(request, 'nutzer.html')

def reservations(request):
    return render(request, 'reservierungen.html')

def support(request):
    return render(request, 'support.html')

def arbeitsplaetze(request):
    return render(request, 'arbeitsplaetze.html', {'workplaces': Workplace.objects.all()})
