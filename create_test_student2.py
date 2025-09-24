import os
import django

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maya_uni.settings')
django.setup()

from malla.models import Student, Career

# Get the career
career = Career.objects.first()

# Create a second test student for semester > 1 testing
student2 = Student.objects.create(
    codigo='EST002',
    career=career,
    current_semester=None,  # Will be set during first login
    first_login_completed=False  # This will trigger the semester setup
)

print(f"Created test student: {student2.codigo} for career: {student2.career.name}")
print(f"First login completed: {student2.first_login_completed}")
print(f"Current semester: {student2.current_semester}")
