#!/usr/bin/env python
"""
Script de prueba para validar la implementación de listas doblemente enlazadas en Django
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maya_uni.settings')
django.setup()

from malla.models import Semester, Subject, Career
from malla.estructura.django_lista import ListaDjangoDobleEnlace

def test_lista_doble_enlace():
    """
    Prueba la funcionalidad básica de la lista doblemente enlazada
    """
    print("=== PRUEBA 1: Lista Doblemente Enlazada Básica ===")
    
    # Crear lista vacía
    lista = ListaDjangoDobleEnlace()
    print(f"Lista vacía - Tamaño: {len(lista)}")
    print(f"¿Está vacía?: {lista.esta_vacia()}")
    
    # Crear algunos objetos de prueba (si existen en la BD)
    try:
        semestres = Semester.objects.all()[:3]
        if semestres:
            print(f"\nAgregando {len(semestres)} semestres a la lista...")
            for semestre in semestres:
                lista.insertar_final(semestre)
            
            print(f"Tamaño después de insertar: {len(lista)}")
            print(f"Primer elemento: {lista.primero()}")
            print(f"Último elemento: {lista.ultimo()}")
            print(f"Recorrido adelante: {lista.recorrerAdelante()}")
            print(f"Recorrido atrás: {lista.recorrerAtras()}")
            
            # Probar iteración
            print("\nIteración con for:")
            for i, semestre in enumerate(lista):
                print(f"  {i}: {semestre}")
            
            # Probar acceso por índice
            print(f"\nAcceso por índice [0]: {lista[0]}")
            if len(lista) > 1:
                print(f"Acceso por índice [1]: {lista[1]}")
        else:
            print("No hay semestres en la base de datos para probar")
    except Exception as e:
        print(f"Error en prueba básica: {e}")

def test_managers():
    """
    Prueba los managers personalizados
    """
    print("\n=== PRUEBA 2: Managers Personalizados ===")
    
    try:
        # Probar manager de semestres
        print("Probando SemesterListaManager...")
        semesters_lista = Semester.lista_objects.all_as_lista()
        print(f"Semestres obtenidos como lista: {len(semesters_lista)}")
        
        if len(semesters_lista) > 0:
            print(f"Primer semestre: {semesters_lista.primero()}")
            print("Iteración sobre semestres:")
            for semestre in semesters_lista:
                print(f"  - {semestre}")
        
        # Probar manager de materias
        print("\nProbando SubjectListaManager...")
        subjects_lista = Subject.lista_objects.all_as_lista()
        print(f"Materias obtenidas como lista: {len(subjects_lista)}")
        
        if len(subjects_lista) > 0:
            print(f"Primera materia: {subjects_lista.primero()}")
            
            # Probar materias recomendadas
            recomendadas = Subject.lista_objects.recomendadas_as_lista(limite=3)
            print(f"Materias recomendadas: {len(recomendadas)}")
            for materia in recomendadas:
                print(f"  - {materia} (Completada: {materia.completed}, Habilitada: {materia.is_enabled()})")
        
    except Exception as e:
        print(f"Error en prueba de managers: {e}")

def test_conversion():
    """
    Prueba las conversiones entre QuerySet y Lista
    """
    print("\n=== PRUEBA 3: Conversiones QuerySet <-> Lista ===")
    
    try:
        # QuerySet a Lista
        queryset = Semester.objects.all()[:2]
        lista = ListaDjangoDobleEnlace()
        lista.from_queryset(queryset)
        
        print(f"QuerySet original: {len(queryset)} elementos")
        print(f"Lista convertida: {len(lista)} elementos")
        
        # Lista a QuerySet
        if len(lista) > 0:
            queryset_convertido = lista.to_queryset(Semester)
            print(f"QuerySet reconvertido: {len(queryset_convertido)} elementos")
            
        # Lista a lista Python
        lista_python = lista.to_list()
        print(f"Lista Python: {len(lista_python)} elementos")
        print(f"Tipo del primer elemento: {type(lista_python[0]) if lista_python else 'N/A'}")
        
    except Exception as e:
        print(f"Error en prueba de conversiones: {e}")

def test_filtering():
    """
    Prueba las funciones de filtrado
    """
    print("\n=== PRUEBA 4: Filtrado y Búsqueda ===")
    
    try:
        # Obtener todas las materias
        materias_lista = Subject.lista_objects.all_as_lista()
        
        if len(materias_lista) > 0:
            print(f"Total de materias: {len(materias_lista)}")
            
            # Filtrar materias completadas
            completadas = materias_lista.filtrar(lambda x: x.completed)
            print(f"Materias completadas: {len(completadas)}")
            
            # Filtrar materias no completadas
            no_completadas = materias_lista.filtrar(lambda x: not x.completed)
            print(f"Materias no completadas: {len(no_completadas)}")
            
            # Buscar por atributo específico
            if len(materias_lista) > 0:
                primera_materia = materias_lista.primero()
                busqueda = materias_lista.buscar(name=primera_materia.name)
                print(f"Búsqueda por nombre '{primera_materia.name}': {len(busqueda)} resultados")
        
    except Exception as e:
        print(f"Error en prueba de filtrado: {e}")

def main():
    """
    Función principal que ejecuta todas las pruebas
    """
    print("INICIANDO PRUEBAS DE IMPLEMENTACIÓN DE LISTA DOBLEMENTE ENLAZADA")
    print("=" * 70)
    
    test_lista_doble_enlace()
    test_managers()
    test_conversion()
    test_filtering()
    
    print("\n" + "=" * 70)
    print("PRUEBAS COMPLETADAS")
    print("\nSi no hay errores arriba, la implementación está funcionando correctamente!")
    print("Los templates de Django deberían funcionar sin problemas con las listas doblemente enlazadas.")

if __name__ == "__main__":
    main()
