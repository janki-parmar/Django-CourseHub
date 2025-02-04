from django.shortcuts import render
from .models import *
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

            user = UserProfile.objects.create(username = username, email = email, password = password, firstname = firstname, lastname = lastname, role = role)
        
        except Exception as e:
            logger.error(f"Error during user registration: {str(e)}")

    return render(request, 'registraton.html') 


def login(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
    
        try :   
                user = UserProfile.objects.get(username = username) if username else UserProfile.objects.get(email=email)

                if user and user.password == password:
                    return render(request, 'dashboard.html', {'message': 'Login successful'})
                else:
                    return render(request, 'login.html', {'error': 'Invalid credentials'})
        except Exception as e:
            return render(request, 'login.html', {'error': str(e)})

    return render(request, 'login.html')
                
