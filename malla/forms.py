# Importaciones necesarias para definir formularios en Django
from django import forms
from .models import Subject, Semester

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
            allowed_subjects = Subject.objects.filter(
                semester__id__lte=semester.id
            )
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

# Formulario para configurar la carrera (duración y semestres por año)
class CareerSetupForm(forms.Form):
    # Campo para el nombre de la carrera
    career_name = forms.CharField(
        label='Nombre de la Carrera',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    # Campo para el nombre de la universidad
    university_name = forms.CharField(
        label='Nombre de la Universidad',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    # Campo para la duración de la carrera en años (mínimo 1)
    career_years = forms.IntegerField(
        label='Duración de la Carrera (años)',
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    # Campo para el número de semestres por año (mínimo 2)
    semesters_per_year = forms.IntegerField(
        label='Semestres por Año',
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
