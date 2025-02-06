from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .middleware import *

import logging
logger = logging.getLogger(__name__)

# Create your views here.

@csrf_exempt
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

@csrf_exempt
def login(request):
    if request.method == 'POST':

        username_email = request.POST.get('username_email')
        password = request.POST.get('password')

    
        try :   
                if '@' in username_email:
                    user = UserProfile.objects.get(email = username_email)
                else:
                    user = UserProfile.objects.get(username = username_email)

                if check_password(password, user.password):
                      
                      token = encode_jwt(user)
                      
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


@csrf_exempt
def logout(request):
    pass

@csrf_exempt
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@csrf_exempt
@role_based_access
def instructor_dashboard(request):
    # Create JWT token using user_id and user_role from request object
    token = encode_jwt({'id': request.user_id, 'role': request.user_role})

    # Retrieve courses based on user_id (instructor)
    courses = Courses.objects.filter(instructor=request.user_id)
    return render(request, 'instructor_dashboard.html', {'courses': courses, 'token': token})


@csrf_exempt
def student_dashboard(request):
    return render(request,'student_dashboard.html')



########====== instructor
@csrf_exempt
@role_based_access
def create_course(request):
    if request.method == 'POST':
        try:

            title = request.POST['title']
            description = request.POST['description']
            instructor = request.user

            courses = Courses.objects.create(title = title, description = description, instructor = instructor)
            return redirect('instructor_dashboard')  
        
        except Exception as e:
            logger.error(f"Error during creating course: {str(e)}")

    return render(request, 'instructor_dashboard.html') 



                

