# Importaciones necesarias para las vistas y manejo de formularios
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import models
from django.contrib import messages
from .models import Semester, Subject, Student, Career
from .forms import SubjectForm, SemesterForm, CareerCreateForm, StudentLoginForm, StudentRegistrationForm
from .estructura.django_lista import ListaDjangoDobleEnlace

# Vista del inicio de sesión
def login(request):
    context = {'login': True}
    
    if request.method == 'POST':
        login_type = request.POST.get('login_type')
        
        if login_type == 'admin':
            # Manejo del login administrativo
            username = request.POST.get("username")
            password = request.POST.get("password")

            if username == "admin@gmail.com" and password == "12345":
                request.session['isSuperUser'] = True
                request.session['isLogged'] = True
                request.session['userType'] = 'admin'
                return redirect("/malla/full-curriculum/")
            else:
                context['admin_errors'] = True
                
        elif login_type == 'student':
            # Manejo del login de estudiante
            form = StudentLoginForm(request.POST)
            if form.is_valid():
                codigo = form.cleaned_data['codigo']
                try:
                    student = Student.objects.get(codigo=codigo)
                    request.session['isLogged'] = True
                    request.session['isSuperUser'] = False
                    request.session['userType'] = 'student'
                    request.session['studentCode'] = codigo
                    request.session['studentId'] = student.id
                    return redirect("/malla/full-curriculum/")
                except Student.DoesNotExist:
                    context['student_errors'] = 'El código de estudiante no existe.'
            else:
                # Si hay errores en el formulario, mostrarlos
                if form.errors.get('codigo'):
                    context['student_errors'] = form.errors['codigo'][0]
                else:
                    context['student_errors'] = 'Error en el formulario.'
        
    return render(request, "malla/login.html", context)

# Vista para registro de estudiantes
def student_register(request):
    context = {'register': True}
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data['codigo']
            career = form.cleaned_data['career']
            # Crear el nuevo estudiante con la carrera seleccionada
            Student.objects.create(codigo=codigo, career=career)
            # Mensaje de éxito
            messages.success(request, f'¡Registro exitoso! Ya puedes iniciar sesión con el código {codigo} para la carrera {career.name}')
            return redirect('malla:login')
        else:
            # Si hay errores en el formulario, mostrarlos
            if form.errors.get('codigo'):
                context['registration_errors'] = form.errors['codigo'][0]
            elif form.errors.get('career'):
                context['registration_errors'] = form.errors['career'][0]
            else:
                context['registration_errors'] = 'Error en el formulario.'
    else:
        form = StudentRegistrationForm()
    
    context['form'] = form
    return render(request, "malla/student_register.html", context)

def logoutSession(request):
    if request.method == 'POST':
        request.session.flush()
        return redirect("malla:login")

# Vista para manejar materias en múltiples semestres
def multi_semester_subjects(request, semester_id=None):
    isSuperUser = request.session.get("isSuperUser")
    isLogged = request.session.get("isLogged")
    # Si se especifica un semestre, se trabaja solo con ese semestre
    if semester_id:
        semester_obj = Semester.objects.get(id=semester_id)
        semesters = ListaDjangoDobleEnlace()
        semesters.insertar_final(semester_obj)
    else:
        # Si no, se obtienen todos los semestres ordenados por id usando lista doblemente enlazada
        semesters = Semester.lista_objects.ordenados_por_id_as_lista()
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
            current_semester = semesters.primero()
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
            'isSuperUser': isSuperUser, 'isLogged': isLogged
        })

# Vista para crear carreras (solo administradores)
def career_setup(request):
    isSuperUser = request.session.get("isSuperUser")
    isLogged = request.session.get("isLogged")

    if not isLogged or not isSuperUser:
        return redirect("/malla/login")

    # Obtener todas las carreras existentes
    careers = Career.objects.all()
    
    if request.method == 'POST':
        form = CareerCreateForm(request.POST)
        if form.is_valid():
            # Crear la nueva carrera
            career = form.save()
            years = form.cleaned_data['career_years']
            semesters_per_year = form.cleaned_data['semesters_per_year']
            
            # Crear semestres según años y semestres por año (con numeración consecutiva)
            for year in range(1, years + 1):
                for sem in range(1, semesters_per_year + 1):
                    # Calcular el número de semestre global consecutivo
                    global_semester_number = (year - 1) * semesters_per_year + sem
                    Semester.objects.create(name=f'Year {year} Semester {global_semester_number}')
            
            messages.success(request, f'¡Carrera "{career.name}" creada exitosamente con {years} años y {semesters_per_year} semestres por año!')
            return redirect('malla:career_setup')
    else:
        form = CareerCreateForm()
    
    return render(request, 'malla/career_setup.html', {
        'form': form, 
        'careers': careers,
        'isSuperUser': isSuperUser, 
        'isLogged': isLogged
    })

# Vista para listar todos los semestres
def semester_list(request):
    isSuperUser = request.session.get("isSuperUser")
    isLogged = request.session.get("isLogged")
    # Usar lista doblemente enlazada en lugar de QuerySet
    semesters = Semester.lista_objects.all_as_lista()
    return render(request, 'malla/semester_list.html', {'semesters': semesters, 'isSuperUser': isSuperUser, 'isLogged': isLogged})

# Vista para crear un nuevo semestre
def create_semester(request):
    isSuperUser = request.session.get("isSuperUser")
    isLogged = request.session.get("isLogged")

    if not isLogged:
        return redirect("/malla/login")
    
    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('malla:semester_list')
    else:
        form = SemesterForm()
    return render(request, 'malla/create_semester.html', {'form': form, 'isSuperUser': isSuperUser, 'isLogged': isLogged})

# Vista para listar materias de un semestre específico
def subject_list(request, semester_id):
    isSuperUser = request.session.get("isSuperUser")
    isLogged = request.session.get("isLogged")
    semester = Semester.objects.get(id=semester_id)
    # Usar lista doblemente enlazada para las materias
    subjects = Subject.lista_objects.ordenadas_por_orden_as_lista(semester)
    return render(request, 'malla/subject_list.html', {'semester': semester, 'subjects': subjects,'isSuperUser': isSuperUser, 'isLogged': isLogged})

# Vista para crear una materia en un semestre específico
def create_subject(request, semester_id):
    isSuperUser = request.session.get("isSuperUser")
    isLogged = request.session.get("isLogged")
    
    if not isLogged:
        return redirect("/malla/login")

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
    return render(request, 'malla/create_subject.html', {'form': form, 'semester': semester, 'isSuperUser': isSuperUser, 'isLogged': isLogged})

# Vista para mostrar la malla completa con materias ordenadas y recomendaciones
def full_curriculum(request):
    isSuperUser = request.session.get("isSuperUser")
    isLogged = request.session.get("isLogged")
    userType = request.session.get("userType")
    
    # Determinar qué carrera mostrar según el tipo de usuario
    if userType == 'student':
        # Si es estudiante, obtener su carrera específica
        studentId = request.session.get("studentId")
        try:
            student = Student.objects.get(id=studentId)
            career = student.career if student.career else Career.objects.first()
        except Student.DoesNotExist:
            career = Career.objects.first()
    else:
        # Si es admin o no hay tipo específico, mostrar la primera carrera
        career = Career.objects.first()
    
    # Obtener todos los semestres ordenados por id usando lista doblemente enlazada
    semesters = Semester.lista_objects.ordenados_por_id_as_lista()
    from itertools import groupby
    grouped_semesters = {}
    # Agrupar semestres por año (extraído del nombre)
    # Convertir a lista Python para usar groupby
    semesters_list = semesters.to_list()
    for key, group in groupby(semesters_list, lambda s: s.name.split()[1] if len(s.name.split()) > 1 else '1'):
        # Convertir cada grupo a lista doblemente enlazada
        grupo_lista = ListaDjangoDobleEnlace()
        grupo_lista.from_list(list(group))
        grouped_semesters[key] = grupo_lista
    # Las materias ya se ordenan en la propiedad ordered_subjects del modelo Semester
    # Obtener materias recomendadas usando lista doblemente enlazada
    recommended_subjects = Subject.lista_objects.recomendadas_as_lista(limite=5)
    # Renderizar plantilla con semestres agrupados, recomendaciones y carrera
    return render(request, 'malla/full_curriculum.html', {'grouped_semesters': grouped_semesters, 'recommended_subjects': recommended_subjects, 'career': career, 'isSuperUser': isSuperUser, 'isLogged': isLogged})

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
