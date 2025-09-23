"""
URLs para la aplicación Malla con autenticación y permisos de administrador
"""
from django.urls import path
from . import views

app_name = 'malla'

urlpatterns = [
    path('login/', views.login, name="login"),
    path('student-register/', views.student_register, name="student_register"),
    path('logout/', views.logoutSession, name="logout"),
    path('career-setup/', views.career_setup, name='career_setup'),
    path('semesters/', views.semester_list, name='semester_list'),
    path('semesters/create/', views.create_semester, name='create_semester'),
    path('semesters/<int:semester_id>/subjects/', views.subject_list, name='subject_list'),
    path('semesters/<int:semester_id>/subjects/create/', views.create_subject, name='create_subject'),
    path('multi-semester-subjects/', views.multi_semester_subjects, name='multi_semester_subjects'),
    path('multi-semester-subjects/<int:semester_id>/', views.multi_semester_subjects, name='multi_semester_subjects_single'),
    path('full-curriculum/', views.full_curriculum, name='full_curriculum'),
    path('toggle-subject/<int:subject_id>/', views.toggle_subject, name='toggle_subject'),
]
