from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt

from .models import *

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
                      request.session['user_id'] = user.id

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




########====== instructor
@csrf_exempt
def instructor_dashboard(request):

    instructor = UserProfile.objects.get(id=request.session.get('user_id'))
    
    if instructor.role == 'instructor':
        courses = Courses.objects.filter(instructor=instructor)

        return render(request, 'instructor_dashboard.html', {'courses': courses})
    

@csrf_exempt
def create_course(request):
    if request.method == 'POST':
        try:

            title = request.POST['title']
            description = request.POST['description']

            instructor = UserProfile.objects.get(id=request.session.get('user_id'))
            
            courses = Courses.objects.create(title = title, description = description, instructor = instructor)
    
            return redirect('instructor_dashboard')  
        
        except Exception as e:
            logger.error(f"Error during creating course: {str(e)}")

    return render(request, 'create_course_form.html') 


@csrf_exempt
def create_course_form(request):
    return render(request, 'create_course_form.html')

@csrf_exempt
def update_course(request):

    if request.method == 'POST':
        pass
        


########====== student
@csrf_exempt
def student_dashboard(request):
    student = UserProfile.objects.get(id=request.session.get('user_id'))
    
    # Tab selection logic based on the query parameter
    selected_tab = request.GET.get('tab', 'available')
    
    courses = Courses.objects.all() if selected_tab == 'available' else []
    enrollments = Enrollment.objects.filter(student=student) if selected_tab == 'enrolled' else []

    context = {
        'student': student,
        'courses': courses,
        'enrollments': enrollments,
        'selected_tab': selected_tab  # Pass selected tab to the template
    }

    return render(request, 'student_dashboard.html', context)


@csrf_exempt
def enroll(request, course_id):

    if request.method == 'POST': 
        student = UserProfile.objects.get(id=request.session.get('user_id'))
        course = get_object_or_404(Courses, id=course_id)
        
        # Check if already enrolled
        if not Enrollment.objects.filter(student=student, course=course).exists():
            Enrollment.objects.create(student=student, course=course)

    return redirect('student_dashboard')
    


                

