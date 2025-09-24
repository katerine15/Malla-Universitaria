#!/usr/bin/env python3
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maya_uni.settings')
django.setup()

from malla.models import Student, Career

def create_test_student():
    print("Creating test student...")
    
    # Get or create a career first
    career, created = Career.objects.get_or_create(
        name="Ingeniería Informática",
        defaults={
            'university': "Colegio Mayor del Cauca"
        }
    )
    
    if created:
        print(f"Created career: {career.name}")
    else:
        print(f"Using existing career: {career.name}")
    
    # Create a test student
    student, created = Student.objects.get_or_create(
        codigo="EST001",
        defaults={
            'career': career,
            'current_semester': None,  # This should be None for first-time login
            'first_login_completed': False  # This should be False for first-time login
        }
    )
    
    if created:
        print(f"Created student: {student.codigo}")
        print(f"Student career: {student.career.name}")
        print(f"Current semester: {student.current_semester}")
        print(f"First login completed: {student.first_login_completed}")
    else:
        print(f"Student {student.codigo} already exists")
        # Update the student to ensure it's set up for first-time login testing
        student.current_semester = None
        student.first_login_completed = False
        student.save()
        print("Updated student for first-time login testing")
    
    print("Test student creation complete!")

if __name__ == "__main__":
    create_test_student()
