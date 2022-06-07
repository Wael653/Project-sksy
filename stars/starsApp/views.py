from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.forms.models import model_to_dict
from stars import templates

# Create your views here.
def index(request):
    return render(request, 'index.html')