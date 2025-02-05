from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.hashers import make_password, check_password
import logging
logger = logging.getLogger(__name__)

# Create your views here.


def registration(request):
    if request.method == 'POST':
        try :
            username = request.POST['username']
            email = request.POST['email']
            password = request. POST['password']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            role = request.POST['role']

            hash_password = make_password(password)
            user = UserProfile.objects.create(username = username, email = email, password = hash_password, firstname = firstname, lastname = lastname, role = role)

            return redirect('login')  
        
        except Exception as e:
            logger.error(f"Error during user registration: {str(e)}")

    return render(request, 'registration.html') 


def login(request):
    if request.method == 'POST':

        username_email = request.POST.get('username_email')
        password = request.POST.get('password')

    
        try :   
                if '@' in username_email:
                    user = UserProfile.objects.get(email = username_email)
                    print("=------------emiallll")
                else:
                    user = UserProfile.objects.get(username = username_email)
                    print("=------------name")

                if check_password(password, user.password):
                    if user.role == 'admin':
                        return redirect('admin_dashboard') 
                    elif user.role == 'instructor':
                        return redirect('instructor_dashboard')
                    elif user.role == 'student':
                        return redirect('student_dashboard')
                    else:
                        return render(request, 'login.html', {'error': 'Role not defined'})
                   
                else:
                    return render(request, 'login.html', {'error': 'Invalid credentials'})
        except Exception as e:
            return render(request, 'login.html', {'error': str(e)})

    return render(request, 'login.html')


def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def instructor_dashboard(request):
    return render(request, 'instructor_dashboard.html')

def student_dashboard(request):
    return render(request,'student_dashboard.html')
                

