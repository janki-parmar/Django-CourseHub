from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('registration', views.registration, name= 'registration'),
    path('logout', views.logout, name= 'logout'),
    path('dashboard/admin', views.admin_dashboard, name= 'admin_dashboard'),
    path('dashboard/instructor', views.instructor_dashboard, name= 'instructor_dashboard'),
    path('dashboard/student', views.student_dashboard, name= 'student_dashboard'),

    path('create_course', views.create_course, name= 'create_course'),
    path('create_course_form', views.create_course_form, name= 'create_course_form'),
    path('update_course/<int:course_id>', views.update_course, name= 'update_course'),
    path('delete_course/<int:course_id>', views.delete_course, name= 'delete_course'),
    


    path('enroll/<int:course_id>', views.enroll, name= 'enroll'),
]