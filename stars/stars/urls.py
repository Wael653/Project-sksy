"""stars URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from starsApp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('myregist', views.myreg, name = 'myregs'),    
    path('impressum/', views.imprint, name='imprint'),
    path('nutzer/', views.user, name='user'),
    path('nutzer/delete/<nutzername>', views.delete_User, name='delete-user'),
    path('reservierungen/', views.reservations, name='reservations'),
    path('reservieren/', views.reservieren, name='reservieren'),
    path('support/', views.support, name='support'),
    path('arbeitsplaetze/', views.arbeitsplaetze, name='arbeitsplaetze'),
    path('registrieren/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('settings/profile/', views.change_profile, name='profile'),
    path('settings/password/', views.change_password, name='password'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('accounts/login_user/', views.login, name="login"),

]
