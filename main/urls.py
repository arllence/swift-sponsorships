"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from account.views import *
from sponsorship.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
	# include urls from account app
    path('account/', include('account.urls')),
    # homepage
    path('', home, name='homepage'),
    # student bio
    path('student/bio', student_bio, name='student_bio'),
    # view pending applications
    path('applicants/pending', view_pending, name='view_pending'),
    # view approved applications
    path('applicants/approved', view_approved, name='view_approved'),
    # sponsor applicant
    path('applicant/sponsor/<int:user_id>', sponsor, name='sponsor'),
    # view student profile
    path('student/<int:user_id>', student_profile, name='student_profile'),
    # approve applicants
    path('approve/<int:user_id>', approve, name='approve'),
    # become staff
    path('create/staff', create_staff, name='create_staff'),

]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()