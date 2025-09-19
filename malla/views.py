from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Semester, Subject
from .forms import SubjectForm, SemesterForm, CareerSetupForm

def multi_semester_subjects(request, semester_id=None):
    if semester_id:
        semesters = [Semester.objects.get(id=semester_id)]
    else:
        semesters = list(Semester.objects.order_by('id'))
    single_semester = len(semesters) == 1
    if request.method == 'POST':
        # Process submitted subjects for all semesters
        for semester in semesters:
            i = 0
            while True:
                name_key = f'semester_{semester.id}_name_{i}'
                prereq_key = f'semester_{semester.id}_prerequisites_{i}'
                if name_key not in request.POST:
                    break
                name = request.POST.get(name_key).strip()
                prereq_names = request.POST.get(prereq_key, '').strip()
                if name:
                    subject = Subject(name=name, semester=semester)
                    subject.prev_subject = None
                    subject.next_subject = None
                    subject.save()
                    if prereq_names:
                        prereq_list = [p.strip() for p in prereq_names.split(',') if p.strip()]
                        prereq_subjects = Subject.objects.filter(name__in=prereq_list)
                        subject.prerequisites.set(prereq_subjects)
                i += 1
        if single_semester:
            current_semester = semesters[0]
            next_semester = Semester.objects.filter(id__gt=current_semester.id).order_by('id').first()
            if next_semester:
                return redirect('malla:multi_semester_subjects_single', semester_id=next_semester.id)
            else:
                return redirect('malla:semester_list')
        else:
            return redirect('malla:semester_list')
    else:
        # Prepare empty forms per semester
        forms_per_semester = {semester.id: SubjectForm(prefix=f'semester_{semester.id}') for semester in semesters}
        return render(request, 'malla/multi_semester_subjects.html', {
            'semesters': semesters,
            'forms_per_semester': forms_per_semester,
            'single_semester': single_semester,
        })

def career_setup(request):
    if request.method == 'POST':
        form = CareerSetupForm(request.POST)
        if form.is_valid():
            years = form.cleaned_data['career_years']
            semesters_per_year = form.cleaned_data['semesters_per_year']
            for year in range(1, years + 1):
                for sem in range(1, semesters_per_year + 1):
                    Semester.objects.create(name=f'Year {year} Semester {sem}')
            first_semester = Semester.objects.order_by('id').first()
            return redirect('malla:multi_semester_subjects_single', semester_id=first_semester.id)
    else:
        form = CareerSetupForm()
    return render(request, 'malla/career_setup.html', {'form': form})

def semester_list(request):
    semesters = Semester.objects.all()
    return render(request, 'malla/semester_list.html', {'semesters': semesters})

def create_semester(request):
    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('malla:semester_list')
    else:
        form = SemesterForm()
    return render(request, 'malla/create_semester.html', {'form': form})

def subject_list(request, semester_id):
    semester = Semester.objects.get(id=semester_id)
    subjects = Subject.objects.filter(semester=semester)
    return render(request, 'malla/subject_list.html', {'semester': semester, 'subjects': subjects})

def create_subject(request, semester_id):
    semester = Semester.objects.get(id=semester_id)
    if request.method == 'POST':
        form = SubjectForm(request.POST, semester=semester)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.semester = semester
            subject.save()
            form.save_m2m()
            return redirect('malla:subject_list', semester_id=semester_id)
    else:
        form = SubjectForm(semester=semester)
    return render(request, 'malla/create_subject.html', {'form': form, 'semester': semester})

def full_curriculum(request):
    semesters = Semester.objects.all().order_by('id')
    from itertools import groupby
    grouped_semesters = {}
    for key, group in groupby(semesters, lambda s: s.name.split()[1] if len(s.name.split()) > 1 else '1'):
        grouped_semesters[key] = list(group)
    return render(request, 'malla/full_curriculum.html', {'grouped_semesters': grouped_semesters})

def toggle_subject(request, subject_id):
    if request.method == 'POST':
        subject = Subject.objects.get(id=subject_id)
        subject.completed = not subject.completed
        subject.save()
        return JsonResponse({'completed': subject.completed})
    return JsonResponse({'error': 'Invalid method'}, status=400)
