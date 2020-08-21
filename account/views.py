from .models import *
import re,random,string
from django.contrib import auth
from sponsorship.models import *
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.template.context_processors import csrf
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# Create your views here.
def get_random_alphanumeric_string(length):
	letters_and_digits = string.ascii_lowercase + string.digits
	result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
	return result_str

def login_(request, *args, **kwargs):
	if request.method == "POST":
		email = request.POST.get('email').strip()
		password = request.POST.get('password').strip()

		if email == '' or password == '':
			messages.error(request, "Whoops, fill all blanks!")
			return redirect(request.META['HTTP_REFERER'])

		if User.objects.filter(email=email).exists():
			user = User.objects.get(email=email)
			username = user.username
			user_id = user.id
		else:
			messages.error(request, "Whoops, invalid email!")
			return redirect(request.META['HTTP_REFERER'])

		user = authenticate(username=username, password=password)

		if user is not None:
			login(request, user)
			try:
				url = request.META['HTTP_REFERER'].split('=')
				url = url[1]
				return redirect(url)
			except IndexError:
				return redirect('homepage')				
		else:
			try:
				user = User.objects.get(email=email)
				if user:
					if user.is_active == 0:
						messages.error(request, "Sorry, your account has been disabled. Contact support!")
						return redirect('account:contact_support')
					else:
						messages.error(request, "Whoops, invalid password !")
						return redirect(request.META['HTTP_REFERER'])
			except:
				messages.error(request, "Whoops, account doesn't exist !")
				return redirect(request.META['HTTP_REFERER'])           
	else:
		return render(request, "account/login.html")

	
def register(request, *args, **kwargs):
	if request.method == "POST":
		category = request.POST.get('user_status').strip().capitalize()
		first_name = request.POST.get('firstname').strip().capitalize()
		last_name = request.POST.get('lastname').strip().capitalize()
		password1 = request.POST.get('password1').strip()
		password2 = request.POST.get('password2').strip()
		email = request.POST.get('email').strip()

		if first_name == '' or last_name == '' or password1 == '' or password2 == '' or email == '' or category == '':
			messages.error(request, "Whoops, fill all blanks !")
			return redirect('/')

		length = random.randint(4,8)
		username = get_random_alphanumeric_string(length)
				
		check = [first_name,last_name]
	
		for data in check:
			x = re.findall("[/\(\*\!\)\-\+\%\@\#\$\%\^\&]", data)
			if (x):
				messages.error(request, "Whoops! Only use A-Z and '_' characters for your names!")
				return redirect(request.META['HTTP_REFERER'])

		if password1 == password2: # checks if passwords match

			if len(password1) < 6:
				messages.error(request, "Whoops! Password must be atleast 6 characters!")
				return redirect(request.META['HTTP_REFERER'])

			if User.objects.filter(email=email).exists():
				messages.error(request, "Whoops! Email already in use, try logging in !")
				return redirect(request.META['HTTP_REFERER'])
			else:
				user = User.objects.create_user(username=username, password=password1,email=email,first_name=first_name,last_name=last_name)
				user.save()

				# login user
				user = authenticate(username=username, password=password1)
				login(request, user)

				# get saved user obj
				saved_user = User.objects.get(username=username)
				if category == "Student":
					data = Student(user=saved_user)
					data.save()
					return redirect('homepage')
				elif category == "Sponsor":
					data = Sponsor(user=saved_user)
					data.save()
					return redirect('homepage')
				else:
					messages.error(request, "Whoops, unknown category!")
					return redirect(request.META['HTTP_REFERER'])
		else:
			messages.error(request, "Whoops! Passwords not matching !")
			return redirect(request.META['HTTP_REFERER'])
	else:
		return render(request, "account/register.html")


def logout_(request, *args, **kwargs):
	logout(request)
	return redirect('account:login')



# IMPORT EMAIL SENDER
from account.sender import smtp_connection, read_template, sender
# Password reset, lost password.
def email_password_reset(request, *args, **kwargs):
	if request.method == "POST":
		email = request.POST.get('email').strip()

		if email == '':
			messages.error(request, "Whoops, email is required!")
			return redirect(request.META['HTTP_REFERER'])


		if User.objects.filter(email=email).exists():
			user_obj = User.objects.filter(email=email)
			user_id = user_obj[0].id
			username = user_obj[0].first_name

			sent = Sent_Codes.objects.filter(user=user_id,status=1)
			if sent:
				code = sent[0].code
			else:
				code = Codes.objects.all()[:1]
				code = code[0].code
				# # print(code) 
			# send reset email link via email
			sender(username,email,code)
			# SAVE SENT CODE
			data = Sent_Codes(user=user_obj[0],code=code)
			data.save()

			messages.success(request, "Success, check your email for account reset link")
			return redirect(request.META['HTTP_REFERER'])

		else:
			messages.error(request, "Whoops, no user with that email!")
			return redirect(request.META['HTTP_REFERER'])

	else:
		return render(request, "password_reset/password_reset.html")


# Password reset, lost password.
def email_new_password(request, mail, code):

	if request.method == "POST":
		password1 = request.POST.get('password1').strip()
		password2 = request.POST.get('password2').strip()

		if password1 == '' or password2 == '':
			messages.error(request, "Whoops, fill all blanks !")
			return redirect(request.META['HTTP_REFERER'])

		if password1 == password2:

			if len(password1) < 6:
				messages.error(request, "Whoops! Password must be atleast 6 characters !")
				return redirect(request.META['HTTP_REFERER'])

			if User.objects.filter(email=mail).exists():
				user_obj = User.objects.filter(email=mail)
				user_id = user_obj[0].id
				username = user_obj[0].username
							
				user = User.objects.get(id=user_id)
				user.password = make_password(password1)
				user.save()
			else:
				messages.error(request, "Whoops! No user found!")
				return redirect('account:email_reset_password')

			user = authenticate(username=username, password=password1)
			login(request, user)

			sent_code = Codes.objects.filter(code=str(code))
			if sent_code:
				sent_code.delete()
			saved = Sent_Codes.objects.filter(code=str(code))
			# print(saved)
			if saved:
				# print(saved)
				saved = saved[0]
				saved.status = False
				saved.save()

			messages.success(request, "Password reset success!")
			return redirect('feed')

		else:
			messages.error(request, "Whoops! Passwords not matching!")
			return redirect(request.META['HTTP_REFERER'])
	else:
		if mail and code:
			context = {
				"mail" : mail,
				"code" : code,
			}
			return render(request, "password_reset/new_password.html", context)
		else:
			return redirect('account:email_reset_password')


# random number generator
@login_required(login_url='/')
def generator(request, *args, **kwargs):
	import random
	if request.method == "POST":
		total = request.POST.get('total').strip()
		total = int(total)

		for i in range(0,total):
			code = random.randint(1000, 100000)
			data = Codes(code=code)
			data.save()
		
		messages.success(request, "Codes generated successfully 😃")
		return redirect(request.META['HTTP_REFERER'])   
	else:
		total = Codes.objects.all().count()
		context = {
			"total" : total,
		}
		return render(request, "admin/generator.html", context)


# Password reset, change password.
@login_required(login_url='/')
def change_password(request, *args, **kwargs):
	if request.method == "POST":
		new_password1 = request.POST.get('new_password1').strip()
		new_password2 = request.POST.get('new_password2').strip()
		current_password = request.POST.get('current_password').strip()


		if new_password1 == '' or new_password2 == '' or current_password == '':
			messages.error(request, "Whoops! Fill all blanks !")
			return redirect(request.META['HTTP_REFERER'])

		# try authenticating to check if current password is right
		user = authenticate(username=request.user.username, password=current_password)

		if user is not None:
			if new_password1 == new_password2:
				if len(new_password1) < 6:
					messages.error(request, "Whoops! Password must be at least 6 characters!")
					return redirect(request.META['HTTP_REFERER'])

				if User.objects.filter(username=request.user.username).exists():
					user_obj = User.objects.filter(username=request.user.username)
					user_id = user_obj[0].id
								
					user = User.objects.get(id=user_id)
					user.password = make_password(new_password1)
					user.save()

					messages.success(request, "Password reset success!")

					user_auth = authenticate(username=request.user.username, password=new_password1)
					login(request, user_auth)

					return redirect(request.META['HTTP_REFERER'])
				else:
					messages.error(request, "Whoops! No user found!")
					return redirect('account:reset_password')
			else:
				messages.error(request, "Whoops! Passwords not matching!")
				return redirect(request.META['HTTP_REFERER'])
		else:
			messages.error(request, "Whoops! That's not your current password")
			return redirect(request.META['HTTP_REFERER'])
			

# Contact support.
def contact_support(request, *args, **kwargs):
	if request.method == "POST":
		email = request.POST.get('email').strip()
		message = request.POST.get('message').strip()
	
		if email == '' or message == '':
			messages.error(request, "Whoops, fill all blanks !")
			return redirect(request.META['HTTP_REFERER'])
		
		try:
			u_id = User.objects.get(id=request.user.id)
		except:
			u_id = None
		
		data_s = Contact_support(user=u_id, email=email, message=message)
		data_s.save()

		messages.success(request, "Message sent successfully, we'll contact you ASAP !")
		return redirect(request.META['HTTP_REFERER'])

	else:
		return render(request, "account/contact_support.html")



def register_edit(request, *args, **kwargs):
	if request.method == "POST":
		first_name = request.POST.get('first_name').strip().capitalize()
		last_name = request.POST.get('last_name').strip().capitalize()
		email = request.POST.get('email').strip()

		if first_name == '' or last_name == '' or email == '':
			messages.error(request, "Whoops! Fill all blanks!")
			return redirect(request.META['HTTP_REFERER'])

		
		check = [first_name,last_name]
	
		for data in check:
			x = re.findall("[/\(\*\!\)\-\+\%\@\#\$\%\^\&]", data)
			if (x):
				# print("YES! We have a match!")
				messages.error(request, "Whoops! Only use A-Z and '_' characters!")
				return redirect(request.META['HTTP_REFERER'])

		u_id = request.user.id
		edit = User.objects.get(id=u_id)
	
		if User.objects.filter(email=email).exists():
			if edit.email == email:
				pass
			else:
				messages.error(request, "Whoops, email already in use !")
				return redirect(request.META['HTTP_REFERER'])
		

		edit.first_name = first_name
		edit.last_name = last_name
		edit.email = email
		edit.save()

		messages.success(request, "Nice, profile update success")
		return redirect(request.META['HTTP_REFERER'])
	else:
		return redirect(request.META['HTTP_REFERER'])