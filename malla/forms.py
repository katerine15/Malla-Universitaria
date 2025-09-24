# Importaciones necesarias para definir formularios en Django
from django import forms
from .models import Subject, Semester, Student, Career
from .estructura.django_lista import ListaDjangoDobleEnlace

# Formulario para crear o editar una materia
class SubjectForm(forms.ModelForm):
    class Meta:
        # Modelo base para el formulario
        model = Subject
        # Campos del modelo que se incluirán en el formulario
        fields = ['name', 'prerequisites']
        # Widgets para personalizar la apariencia de los campos
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'prerequisites': forms.CheckboxSelectMultiple,
        }

    # Método de inicialización para personalizar el formulario
    def __init__(self, *args, **kwargs):
        # Extraer el semestre del kwargs (pasado desde la vista)
        semester = kwargs.pop('semester', None)
        super().__init__(*args, **kwargs)
        if semester:
            # Limitar los prerrequisitos a materias del mismo semestre o anteriores
            # Esto evita que se seleccionen prerrequisitos de semestres futuros
            # Usar lista doblemente enlazada para obtener materias permitidas
            allowed_subjects_lista = Subject.lista_objects.filter_as_lista(
                semester__id__lte=semester.id
            )
            # Convertir la lista doblemente enlazada a QuerySet para compatibilidad con el formulario
            allowed_subjects = allowed_subjects_lista.to_queryset(Subject)
            # Asignar el queryset filtrado al campo de prerrequisitos
            self.fields['prerequisites'].queryset = allowed_subjects

# Formulario para crear o editar un semestre
class SemesterForm(forms.ModelForm):
    class Meta:
        # Modelo base para el formulario
        model = Semester
        # Campos del modelo que se incluirán en el formulario
        fields = ['name']
        # Widgets para personalizar la apariencia de los campos
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Formulario para crear carreras (solo administradores)
class CareerCreateForm(forms.ModelForm):
    # Campo para la duración de la carrera en años (mínimo 1)
    career_years = forms.IntegerField(
        label='Duración de la Carrera (años)',
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    # Campo para el número de semestres por año (mínimo 1)
    semesters_per_year = forms.IntegerField(
        label='Semestres por Año',
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Career
        fields = ['name', 'university']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'university': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nombre de la Carrera',
            'university': 'Nombre de la Universidad',
        }

# Formulario para login de estudiantes
class StudentLoginForm(forms.Form):
    # Campo para el código del estudiante
    codigo = forms.CharField(
        label='Código de Estudiante',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu código de estudiante'
        })
    )

    def clean_codigo(self):
        """
        Validar que el código del estudiante existe en la base de datos
        """
        codigo = self.cleaned_data['codigo']
        try:
            Student.objects.get(codigo=codigo)
        except Student.DoesNotExist:
            raise forms.ValidationError('El código de estudiante no existe.')
        return codigo

# Formulario para registro de estudiantes
class StudentRegistrationForm(forms.Form):
    # Campo para el código del estudiante
    codigo = forms.CharField(
        label='Código de Estudiante',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu código de estudiante'
        })
    )
    # Campo para seleccionar la carrera
    career = forms.ModelChoiceField(
        label='Carrera',
        queryset=Career.objects.all(),
        empty_label='Selecciona una carrera',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean_codigo(self):
        """
        Validar que el código del estudiante no existe ya en la base de datos
        """
        codigo = self.cleaned_data['codigo']
        if Student.objects.filter(codigo=codigo).exists():
            raise forms.ValidationError('Este código de estudiante ya está registrado.')
        return codigo

# Formulario para selección de semestre (primera vez)
class SemesterSelectionForm(forms.Form):
    current_semester = forms.IntegerField(
        label='¿En qué semestre te encuentras actualmente?',
        min_value=1,
        max_value=12,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ejemplo: 1, 2, 3...',
            'min': '1',
            'max': '12'
        }),
        help_text='Ingresa el número del semestre en el que te encuentras actualmente'
    )

    def clean_current_semester(self):
        """
        Validar que el semestre esté en un rango válido
        """
        semester = self.cleaned_data['current_semester']
        if semester < 1 or semester > 12:
            raise forms.ValidationError('El semestre debe estar entre 1 y 12.')
        return semester
