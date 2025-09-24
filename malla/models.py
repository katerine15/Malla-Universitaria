
# Importaciones necesarias para definir modelos en Django
from django.db import models
from .managers import CareerListaManager, SemesterListaManager, SubjectListaManager

# Modelo para almacenar la información de la carrera universitaria
class Career(models.Model):
    """
    Modelo para almacenar la información de las carreras universitarias.
    Los administradores pueden crear múltiples carreras.
    """
    name = models.CharField(max_length=200, help_text='Nombre de la carrera')
    university = models.CharField(max_length=200, help_text='Nombre de la universidad')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text='Fecha de creación de la carrera')

    # Managers
    objects = models.Manager()  # Manager por defecto
    lista_objects = CareerListaManager()  # Manager con listas doblemente enlazadas

    def __str__(self):
        return f"{self.name} - {self.university}"

    class Meta:
        verbose_name = 'Carrera'
        verbose_name_plural = 'Carreras'

# Modelo para representar un estudiante
class Student(models.Model):
    """
    Modelo para almacenar la información básica de los estudiantes.
    Solo requiere un código para el login y debe seleccionar una carrera.
    """
    codigo = models.CharField(max_length=20, unique=True, help_text='Código único del estudiante')
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='students', null=True, blank=True, help_text='Carrera del estudiante')
    current_semester = models.PositiveIntegerField(null=True, blank=True, help_text='Semestre actual del estudiante')
    first_login_completed = models.BooleanField(default=False, help_text='Indica si el estudiante ha completado la configuración inicial')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Fecha de creación del registro')

    # Managers
    objects = models.Manager()  # Manager por defecto

    def __str__(self):
        return f"Estudiante {self.codigo} - {self.career.name if self.career else 'Sin carrera'}"

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'

# Modelo para representar un semestre en la malla curricular
class Semester(models.Model):
    # Nombre del semestre (ej: "Year 1 Semester 1")
    name = models.CharField(max_length=100)
    # Relación con el semestre anterior (opcional, se puede dejar vacío)
    prev_semester = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_semester_rel')
    # Relación con el semestre siguiente (opcional, se puede dejar vacío)
    next_semester = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='prev_semester_rel')

    # Managers
    objects = models.Manager()  # Manager por defecto
    lista_objects = SemesterListaManager()  # Manager con listas doblemente enlazadas

    # Método para representar el objeto como cadena (usado en admin y depuración)
    def __str__(self):
        return self.name

    @property
    def ordered_subjects(self):
        """
        Devuelve las materias del semestre ordenadas por el campo order.
        """
        return self.subjects.order_by('order')
    
    @property
    def ordered_subjects_as_lista(self):
        """
        Devuelve las materias del semestre ordenadas como lista doblemente enlazada.
        """
        from .estructura.django_lista import ListaDjangoDobleEnlace
        lista = ListaDjangoDobleEnlace()
        materias_ordenadas = self.subjects.order_by('order')
        return lista.from_queryset(materias_ordenadas)

# Modelo para representar una materia en la malla curricular
class Subject(models.Model):
    # Nombre de la materia
    name = models.CharField(max_length=100)
    # Relación con el semestre al que pertenece la materia (si se elimina el semestre, se eliminan las materias)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='subjects')
    # Relación con la materia anterior en la secuencia (opcional)
    prev_subject = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_subject_rel')
    # Relación con la materia siguiente en la secuencia (opcional)
    next_subject = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='prev_subject_rel')
    # Relación muchos a muchos con prerrequisitos (materias que deben aprobarse antes)
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='required_for')
    # Indicador de si la materia está completada (aprobada)
    completed = models.BooleanField(default=False)
    # Campo para ordenar las materias dentro del semestre (número entero positivo)
    order = models.PositiveIntegerField(default=0)

    # Managers
    objects = models.Manager()  # Manager por defecto
    lista_objects = SubjectListaManager()  # Manager con listas doblemente enlazadas

    # Método para representar el objeto como cadena
    def __str__(self):
        return self.name

    # Método para verificar si la materia está habilitada (todos los prerrequisitos completados)
    def is_enabled(self):
        # Retorna True si todos los prerrequisitos están completados, False en caso contrario
        return all(prereq.completed for prereq in self.prerequisites.all())
