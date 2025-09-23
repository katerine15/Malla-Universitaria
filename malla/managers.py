from django.db import models
from .estructura.django_lista import ListaDjangoDobleEnlace

class ListaDobleEnlaceManager(models.Manager):
    """
    Manager personalizado que devuelve listas doblemente enlazadas en lugar de QuerySets
    """
    
    def all_as_lista(self):
        """
        Devuelve todos los objetos como lista doblemente enlazada
        """
        queryset = self.get_queryset()
        lista = ListaDjangoDobleEnlace()
        return lista.from_queryset(queryset)
    
    def filter_as_lista(self, **kwargs):
        """
        Filtra objetos y devuelve como lista doblemente enlazada
        """
        queryset = self.filter(**kwargs)
        lista = ListaDjangoDobleEnlace()
        return lista.from_queryset(queryset)
    
    def order_by_as_lista(self, *fields):
        """
        Ordena objetos y devuelve como lista doblemente enlazada
        """
        queryset = self.order_by(*fields)
        lista = ListaDjangoDobleEnlace()
        return lista.from_queryset(queryset)
    
    def get_as_lista(self, **kwargs):
        """
        Obtiene un objeto específico y lo devuelve en una lista doblemente enlazada
        """
        obj = self.get(**kwargs)
        lista = ListaDjangoDobleEnlace()
        lista.insertar_final(obj)
        return lista

class SemesterListaManager(ListaDobleEnlaceManager):
    """
    Manager especializado para el modelo Semester
    """
    
    def ordenados_por_id_as_lista(self):
        """
        Devuelve todos los semestres ordenados por ID como lista doblemente enlazada
        """
        return self.order_by_as_lista('id')
    
    def por_año_as_lista(self, año):
        """
        Filtra semestres por año y devuelve como lista doblemente enlazada
        """
        return self.filter_as_lista(name__icontains=f'Year {año}')

class SubjectListaManager(ListaDobleEnlaceManager):
    """
    Manager especializado para el modelo Subject
    """
    
    def por_semestre_as_lista(self, semester):
        """
        Devuelve materias de un semestre específico como lista doblemente enlazada
        """
        return self.filter_as_lista(semester=semester)
    
    def ordenadas_por_orden_as_lista(self, semester):
        """
        Devuelve materias de un semestre ordenadas por el campo 'order'
        """
        queryset = self.filter(semester=semester).order_by('order')
        lista = ListaDjangoDobleEnlace()
        return lista.from_queryset(queryset)
    
    def completadas_as_lista(self):
        """
        Devuelve solo las materias completadas como lista doblemente enlazada
        """
        return self.filter_as_lista(completed=True)
    
    def no_completadas_as_lista(self):
        """
        Devuelve solo las materias no completadas como lista doblemente enlazada
        """
        return self.filter_as_lista(completed=False)
    
    def habilitadas_as_lista(self):
        """
        Devuelve materias habilitadas (con prerrequisitos completados) como lista doblemente enlazada
        """
        # Obtener todas las materias
        todas_materias = self.all()
        lista = ListaDjangoDobleEnlace()
        
        # Filtrar solo las habilitadas
        for materia in todas_materias:
            if materia.is_enabled():
                lista.insertar_final(materia)
        
        return lista
    
    def recomendadas_as_lista(self, limite=5):
        """
        Devuelve materias recomendadas (habilitadas y no completadas) limitadas
        """
        todas_materias = self.all()
        lista = ListaDjangoDobleEnlace()
        contador = 0
        
        for materia in todas_materias:
            if contador >= limite:
                break
            if materia.is_enabled() and not materia.completed:
                lista.insertar_final(materia)
                contador += 1
        
        return lista

class CareerListaManager(ListaDobleEnlaceManager):
    """
    Manager especializado para el modelo Career
    """
    
    def primera_carrera_as_lista(self):
        """
        Devuelve la primera carrera como lista doblemente enlazada
        """
        try:
            carrera = self.first()
            if carrera:
                lista = ListaDjangoDobleEnlace()
                lista.insertar_final(carrera)
                return lista
        except:
            pass
        return ListaDjangoDobleEnlace()  # Lista vacía si no hay carrera
