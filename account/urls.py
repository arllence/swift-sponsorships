"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from account.views import *

app_name = 'account'

urlpatterns = [
    path('register', register, name='register'),
    path('login', login_, name='login'),
    path('logout', logout_, name='logout'),

    # RESET PASSWORD BY EMAIL
    path('email/reset/password', email_password_reset, name='email_reset_password'),
    # path('email/password/reset', email_new_password, name='email_password_reset'),
    path('email/<str:mail>/<int:code>', email_new_password, name='email_password_reset'),

    # CHANGE PASSWORD
    path('change/password', change_password, name='change_password'),

    # CONTACT SUPPORT
    path('contact/support', contact_support, name='contact_support'),

    # EDIT USER OBJ
    path('user/edit', register_edit, name='register_edit'),

    # GENERATE CODE
    path('generator', generator, name='generator'),
]
