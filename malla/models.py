from django.db import models

class Semester(models.Model):
    name = models.CharField(max_length=100)
    prev_semester = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_semester_rel')
    next_semester = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='prev_semester_rel')

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='subjects')
    prev_subject = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_subject_rel')
    next_subject = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='prev_subject_rel')
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='required_for')
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def is_enabled(self):
        return all(prereq.completed for prereq in self.prerequisites.all())
