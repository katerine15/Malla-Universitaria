from django import forms
from .models import Subject, Semester

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'prerequisites']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'prerequisites': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        semester = kwargs.pop('semester', None)
        super().__init__(*args, **kwargs)
        if semester:
            # Limit prerequisites to subjects in the same or previous semesters
            allowed_subjects = Subject.objects.filter(
                semester__id__lte=semester.id
            )
            self.fields['prerequisites'].queryset = allowed_subjects

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CareerSetupForm(forms.Form):
    career_years = forms.IntegerField(
        label='Duración de la Carrera (años)',
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    semesters_per_year = forms.IntegerField(
        label='Semestres por Año',
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
