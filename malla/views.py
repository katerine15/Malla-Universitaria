# Importaciones necesarias para las vistas y manejo de formularios
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import models
from .models import Semester, Subject
from .forms import SubjectForm, SemesterForm, CareerSetupForm

# Vista del inicio de sesión
def login(request):

    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == "admin@gmail.com" and password == "12345":
            request.session['isSuperUser'] = True
            return redirect("/malla/full-curriculum/")
        
    return render(request, "malla/login.html", { 'login': True })

def logoutSession(request):
    request.session.pop("isSuperUser")
    return redirect(request, "/malla/login.html")

# Vista para manejar materias en múltiples semestres
def multi_semester_subjects(request, semester_id=None):
    # Si se especifica un semestre, se trabaja solo con ese semestre
    if semester_id:
        semesters = [Semester.objects.get(id=semester_id)]
    else:
        # Si no, se obtienen todos los semestres ordenados por id
        semesters = list(Semester.objects.order_by('id'))
    single_semester = len(semesters) == 1

    if request.method == 'POST':
        # Procesar las materias enviadas para todos los semestres
        for semester in semesters:
            i = 0
            while True:
                # Claves para obtener nombre y prerrequisitos de la materia en el POST
                name_key = f'semester_{semester.id}_name_{i}'
                prereq_key = f'semester_{semester.id}_prerequisites_{i}'

                # Si no hay más materias, salir del ciclo
                if name_key not in request.POST:
                    break

                # Obtener nombre y prerrequisitos de la materia
                name = request.POST.get(name_key).strip()
                prereq_names = request.POST.get(prereq_key, '').strip()

                if name:
                    # Obtener el orden máximo actual para asignar el siguiente orden
                    max_order = Subject.objects.filter(semester=semester).aggregate(models.Max('order'))['order__max'] or 0
                    # Crear la materia con el orden siguiente
                    subject = Subject(name=name, semester=semester, order=max_order + 1)
                    # Inicializar relaciones previas y siguientes como None
                    subject.prev_subject = None
                    subject.next_subject = None
                    # Guardar la materia
                    subject.save()

                    # Si hay prerrequisitos, asignarlos
                    if prereq_names:
                        prereq_list = [p.strip() for p in prereq_names.split(',') if p.strip()]
                        prereq_subjects = Subject.objects.filter(name__in=prereq_list)
                        subject.prerequisites.set(prereq_subjects)
                i += 1

        # Si solo hay un semestre, redirigir al siguiente semestre o a la lista de semestres
        if single_semester:
            current_semester = semesters[0]
            next_semester = Semester.objects.filter(id__gt=current_semester.id).order_by('id').first()
            if next_semester:
                return redirect('malla:multi_semester_subjects_single', semester_id=next_semester.id)
            else:
                return redirect('malla:semester_list')
        else:
            # Si hay múltiples semestres, redirigir a la lista de semestres
            return redirect('malla:semester_list')
    else:
        # Preparar formularios vacíos para cada semestre
        forms_per_semester = {semester.id: SubjectForm(prefix=f'semester_{semester.id}') for semester in semesters}
        return render(request, 'malla/multi_semester_subjects.html', {
            'semesters': semesters,
            'forms_per_semester': forms_per_semester,
            'single_semester': single_semester,
        })

# Vista para configurar la carrera (años y semestres)
def career_setup(request):
    from .models import Career
    career, created = Career.objects.get_or_create(id=1)
    if request.method == 'POST':
        form = CareerSetupForm(request.POST)
        if form.is_valid():
            career.name = form.cleaned_data['career_name']
            career.university = form.cleaned_data['university_name']
            career.save()
            years = form.cleaned_data['career_years']
            semesters_per_year = form.cleaned_data['semesters_per_year']
            # Crear semestres según años y semestres por año (con numeración consecutiva)
            for year in range(1, years + 1):
                for sem in range(1, semesters_per_year + 1):
                    # Calcular el número de semestre global consecutivo
                    global_semester_number = (year - 1) * semesters_per_year + sem
                    Semester.objects.create(name=f'Year {year} Semester {global_semester_number}')
            # Redirigir al primer semestre creado
            first_semester = Semester.objects.order_by('id').first()
            return redirect('malla:multi_semester_subjects_single', semester_id=first_semester.id)
    else:
        form = CareerSetupForm(initial={'career_name': career.name, 'university_name': career.university})
    return render(request, 'malla/career_setup.html', {'form': form})

# Vista para listar todos los semestres
def semester_list(request):
    semesters = Semester.objects.all()
    return render(request, 'malla/semester_list.html', {'semesters': semesters})

# Vista para crear un nuevo semestre
def create_semester(request):
    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('malla:semester_list')
    else:
        form = SemesterForm()
    return render(request, 'malla/create_semester.html', {'form': form})

# Vista para listar materias de un semestre específico
def subject_list(request, semester_id):
    semester = Semester.objects.get(id=semester_id)
    subjects = Subject.objects.filter(semester=semester)
    return render(request, 'malla/subject_list.html', {'semester': semester, 'subjects': subjects})

# Vista para crear una materia en un semestre específico
def create_subject(request, semester_id):
    semester = Semester.objects.get(id=semester_id)
    if request.method == 'POST':
        form = SubjectForm(request.POST, semester=semester)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.semester = semester
            # Asignar orden siguiente para la materia
            max_order = Subject.objects.filter(semester=semester).aggregate(models.Max('order'))['order__max'] or 0
            subject.order = max_order + 1
            subject.save()
            form.save_m2m()
            return redirect('malla:subject_list', semester_id=semester_id)
    else:
        form = SubjectForm(semester=semester)
    return render(request, 'malla/create_subject.html', {'form': form, 'semester': semester})

# Vista para mostrar la malla completa con materias ordenadas y recomendaciones
def full_curriculum(request):
    isSuperUser = request.session.get("isSuperUser")
    from .models import Career
    career = Career.objects.first()
    # Obtener todos los semestres ordenados por id
    semesters = Semester.objects.all().order_by('id')
    from itertools import groupby
    grouped_semesters = {}
    # Agrupar semestres por año (extraído del nombre)
    for key, group in groupby(semesters, lambda s: s.name.split()[1] if len(s.name.split()) > 1 else '1'):
        grouped_semesters[key] = list(group)
    # Las materias ya se ordenan en la propiedad ordered_subjects del modelo Semester
    # Obtener todas las materias para calcular recomendaciones
    all_subjects = Subject.objects.all()
    # Filtrar materias habilitadas y no completadas, limitar a 5 recomendaciones
    recommended_subjects = [s for s in all_subjects if s.is_enabled() and not s.completed][:5]
    # Renderizar plantilla con semestres agrupados, recomendaciones y carrera
    return render(request, 'malla/full_curriculum.html', {'grouped_semesters': grouped_semesters, 'recommended_subjects': recommended_subjects, 'career': career, 'isSuperUser': isSuperUser})

# Vista para alternar el estado de completado de una materia (activar/desactivar)
def toggle_subject(request, subject_id):
    if request.method == 'POST':
        subject = Subject.objects.get(id=subject_id)
        # Cambiar estado completado al opuesto
        subject.completed = not subject.completed
        if not subject.completed:
            # Si se marca como no completada, mover al final del orden
            max_order = Subject.objects.filter(semester=subject.semester).aggregate(models.Max('order'))['order__max'] or 0
            subject.order = max_order + 1
        subject.save()
        # Responder con el nuevo estado completado
        return JsonResponse({'completed': subject.completed})
    # Si no es POST, devolver error
    return JsonResponse({'error': 'Invalid method'}, status=400)
