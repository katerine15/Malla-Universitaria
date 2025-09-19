# Importaciones necesarias para definir modelos en Django
from django.db import models

# Modelo para almacenar la información de la carrera universitaria
class Career(models.Model):
    """
    Modelo para almacenar la información de la carrera universitaria.
    Se asume que solo hay una carrera por aplicación.
    """
    name = models.CharField(max_length=200, default='Ingeniería Informática', help_text='Nombre de la carrera')
    university = models.CharField(max_length=200, default='Colegio Mayor del Cauca', help_text='Nombre de la universidad')

    def __str__(self):
        return f"{self.name} - {self.university}"

    class Meta:
        verbose_name = 'Carrera'
        verbose_name_plural = 'Carreras'

# Modelo para representar un semestre en la malla curricular
class Semester(models.Model):
    # Nombre del semestre (ej: "Year 1 Semester 1")
    name = models.CharField(max_length=100)
    # Relación con el semestre anterior (opcional, se puede dejar vacío)
    prev_semester = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_semester_rel')
    # Relación con el semestre siguiente (opcional, se puede dejar vacío)
    next_semester = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='prev_semester_rel')

    # Método para representar el objeto como cadena (usado en admin y depuración)
    def __str__(self):
        return self.name

    @property
    def ordered_subjects(self):
        """
        Devuelve las materias del semestre ordenadas por el campo order.
        """
        return self.subjects.order_by('order')

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

    # Método para representar el objeto como cadena
    def __str__(self):
        return self.name

    # Método para verificar si la materia está habilitada (todos los prerrequisitos completados)
    def is_enabled(self):
        # Retorna True si todos los prerrequisitos están completados, False en caso contrario
        return all(prereq.completed for prereq in self.prerequisites.all())
