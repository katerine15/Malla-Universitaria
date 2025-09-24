#!/usr/bin/env python3
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maya_uni.settings')
django.setup()

from malla.models import Career, Semester, Subject

def setup_test_data():
    print("Setting up test data...")
    
    # Check existing data first
    print(f"Existing careers: {Career.objects.count()}")
    print(f"Existing semesters: {Semester.objects.count()}")
    print(f"Existing subjects: {Subject.objects.count()}")
    
    # Create a test career if it doesn't exist
    career, created = Career.objects.get_or_create(
        name="Ingeniería de Sistemas",
        defaults={
            'university': "Universidad Maya"
        }
    )
    
    if created:
        print(f"Created career: {career.name}")
    else:
        print(f"Career already exists: {career.name}")
    
    # Create some basic semesters if they don't exist
    semesters_data = [
        "Year 1 Semester 1",
        "Year 1 Semester 2", 
        "Year 2 Semester 3",
        "Year 2 Semester 4"
    ]
    
    for semester_name in semesters_data:
        semester, created = Semester.objects.get_or_create(
            name=semester_name
        )
        if created:
            print(f"Created semester: {semester.name}")
    
    # Create some basic subjects for first semester
    first_semester = Semester.objects.filter(name="Year 1 Semester 1").first()
    if first_semester:
        subjects_data = [
            "Matemáticas I",
            "Programación I", 
            "Física I",
            "Inglés I"
        ]
        
        for i, subject_name in enumerate(subjects_data, 1):
            subject, created = Subject.objects.get_or_create(
                name=subject_name,
                semester=first_semester,
                defaults={'order': i}
            )
            if created:
                print(f"Created subject: {subject.name}")
    
    # Show final counts
    print(f"Final careers: {Career.objects.count()}")
    print(f"Final semesters: {Semester.objects.count()}")
    print(f"Final subjects: {Subject.objects.count()}")
    
    # List all careers
    print("All careers:")
    for career in Career.objects.all():
        print(f"  - {career.name} ({career.university})")
    
    print("Test data setup complete!")

if __name__ == "__main__":
    setup_test_data()
