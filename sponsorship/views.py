import os
from .models import *
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.utils.decorators import method_decorator
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required



# Create your views here. hmm :)

# gets homepage
def home(request, *args, **kwargs):
	if request.user.is_authenticated:
		if request.user.is_staff:
			return redirect('view_pending')
		else:
			if Student.objects.filter(user=request.user.id).exists():
				if Bio_Data.objects.filter(user=request.user.id).exists():
					user_obj = Student.objects.get(user=request.user.id)
					status = user_obj.status
					context = {
						"applied" : "applied",
						"status": status,
					}
					return render(request,'homepage.html', context)
				return render(request,'homepage.html')
			elif Sponsor.objects.filter(user=request.user.id).exists():
				return redirect('view_approved')	
			else:
				return redirect('account:logout')
	else:
		return redirect('account:login')
		
		
		
# create applicant bio
@login_required(login_url='/')
def student_bio(request, *args, **kwargs):
	if request.method == "POST":
		# student info
		student_address = request.POST.get('student_adress').strip().capitalize()
		phone = request.POST.get('phone').strip()
		birth_cert = request.FILES['bcert']
		national_id = request.FILES['nid']
		# school info
		sch_name = request.POST.get('sch_name').strip().capitalize()
		sch_adress = request.POST.get('student_adress').strip().capitalize()
		academic_level = request.POST.get('alevel').strip()
		completion_year = request.POST.get('year').strip()
		# reasons
		reason = request.POST.get('reason').strip()
		rec_letter = request.FILES['recletter']


		var = [student_address,phone,birth_cert,national_id,sch_name,sch_adress,academic_level,completion_year,reason,rec_letter]

		for data in var:
			if data == '':
				messages.error(request, "Whoops, fill all blanks !")
				return redirect(request.META['HTTP_REFERER'])
		
		# get user obj
		user = User.objects.get(id=request.user.id)		

		fs = FileSystemStorage()
		# get birth_cert filename
		birth_cert_filename = (birth_cert.name, birth_cert)
		birth_cert_filename = (birth_cert.name)
		# get national_id filename
		national_id_filename = (national_id.name, national_id)
		national_id_filename = (national_id.name)
		# get rec_letter filename
		rec_letter_filename = (rec_letter.name, rec_letter)
		rec_letter_filename = (rec_letter.name)
		
		# get file extensions
		birth_cert_ext = os.path.splitext(birth_cert_filename)[1][1:].strip().lower()
		national_id_ext = os.path.splitext(national_id_filename)[1][1:].strip().lower()
		rec_letter_ext = os.path.splitext(rec_letter_filename)[1][1:].strip().lower()

		# check file extensions
		extns = [birth_cert_ext,national_id_ext,rec_letter_ext]
		for data in extns:
			if data not in set(['jpg', 'jpeg', 'png','tiff','tif','pdf','docx','doc']):
				messages.error(request, "Uploaded file format not supported!")
				return redirect(request.META['HTTP_REFERER'])

		# save birth_cert photo
		birth_cert_filename = fs.save(birth_cert.name, birth_cert)
		birth_cert_uploaded_file_url = fs.url(birth_cert_filename)
		
		# save national_id file
		national_id_filename = fs.save(national_id.name, national_id)
		national_id_uploaded_file_url = fs.url(national_id_filename)

		# save rec_letter file
		rec_letter_filename = fs.save(rec_letter.name, rec_letter)
		rec_letter_uploaded_file_url = fs.url(rec_letter_filename)

		# save student data to db
		data = Bio_Data(user=user,address=student_address,phone=phone,birth_certificate=birth_cert_uploaded_file_url,national_id=national_id_uploaded_file_url)
		data.save()
		# save school data to db
		data = School_Info(user=user,name=sch_name,address=sch_adress,academic_level=academic_level,completion_year=completion_year)
		data.save()
		# save reasons data to db
		data = Reasons(user=user,reason=reason,rec_letter=rec_letter_uploaded_file_url)
		data.save()

		# throw message to user
		messages.success(request, f"Saved successfully!")
		return redirect('homepage')
	else:
		return render(request, "student/bio_data.html")


# gets all pending applicants
@login_required(login_url='/')
def view_pending(request, *args, **kwargs):
	if request.user.is_staff:
		pending = Student.objects.filter(status=0)
		context = {
			"pending": pending,
		}
		return render(request,'staff/index.html', context)
	return redirect('homepage')


# gets all approved applicants
@login_required(login_url='/')
def view_approved(request, *args, **kwargs):
	if request.user.is_staff or Sponsor.objects.filter(user=request.user.id).exists():
		# get the non sponsored students first
		approved = Student.objects.filter(status=1).order_by('sponsored')
		context = {
			"approved": approved,
		}
		return render(request,'sponsor/index.html', context)
	return redirect('homepage')


# student profile
@login_required(login_url='/')
def student_profile(request, user_id, *args, **kwargs):
	student = Student.objects.filter(user=user_id)
	bio_data = Bio_Data.objects.filter(user=user_id)
	sch_info = School_Info.objects.filter(user=user_id)
	reason = Reasons.objects.filter(user=user_id)
	
	context = {
		"student":student,
		"bio_data":bio_data,
		"sch_info":sch_info,
		"reason":reason,
	}
	return render(request, "student/profile.html", context)

# import email function
from sponsorship.mailer import *

# Approve student profile
@login_required(login_url='/')
def approve(request, user_id, *args, **kwargs):
	if request.user.is_staff:
		student = Student.objects.filter(user=user_id)
		student = student[0]
		student.status = 1
		student.save()

		# applicant details
		username = student.user.first_name
		email = student.user.email
		action = 'approved'
		# send email to applicant
		sender(username,email,action)

		messages.success(request, f"Approved successfully!")
		return redirect(request.META['HTTP_REFERER'])
	return redirect('homepage')
	

# Approve student profile
@login_required(login_url='/')
def sponsor(request, user_id, *args, **kwargs):
	if Sponsor.objects.filter(user=request.user.id).exists():
		# get sponsor user object
		sponsor = User.objects.get(id=request.user.id)
		# get applicant user object
		user_obj = User.objects.get(id=user_id)
		# get student applicant object
		applicant = Student.objects.filter(user=user_id)
		applicant = applicant[0]
		applicant.sponsored = True # indicate the applicant has been sposored
		applicant.save()

		# save sonsored and sponsor details
		student = Sponsored(user=user_obj,by=sponsor)
		student.save()

		# applicant details
		username = applicant.user.first_name
		email = applicant.user.email
		action = 'sponsored'
		# send email to applicant
		sender(username,email,action)
		
		messages.success(request, f"Sponsor success !")
		return redirect(request.META['HTTP_REFERER'])
	return redirect('homepage')
	
	
# create staff
@login_required(login_url='/')
def create_staff(request, *args, **kwargs):
	user = User.objects.get(id=request.user.id)
	user.is_staff = True
	user.save()
	return redirect('homepage')
