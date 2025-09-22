#!/usr/bin/env python
"""
Script para probar que el error de NoReverseMatch se ha solucionado
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maya_uni.settings')
django.setup()

from django.test import Client
from django.urls import reverse

def test_url_resolution():
    """Probar que las URLs se resuelven correctamente"""
    print("🧪 Probando resolución de URLs...")

    # Probar URLs de autenticación
    auth_urls = ['login', 'logout']
    for url_name in auth_urls:
        try:
            url = reverse(url_name)
            print(f"   ✅ {url_name}: {url}")
        except Exception as e:
            print(f"   ❌ {url_name}: {e}")

    # Probar URLs de la app malla
    malla_urls = [
        'malla:career_setup',
        'malla:semester_list',
        'malla:create_semester',
        'malla:full_curriculum'
    ]

    for url_name in malla_urls:
        try:
            url = reverse(url_name)
            print(f"   ✅ {url_name}: {url}")
        except Exception as e:
            print(f"   ❌ {url_name}: {e}")

def test_template_rendering():
    """Probar que los templates se renderizan sin errores"""
    print("\n🧪 Probando renderizado de templates...")

    client = Client()

    # Probar acceso a páginas principales
    test_urls = [
        ('/malla/career-setup/', 'career_setup'),
        ('/malla/semesters/', 'semester_list'),
        ('/malla/full-curriculum/', 'full_curriculum'),
    ]

    for url, name in test_urls:
        try:
            response = client.get(url)
            if response.status_code == 200:
                print(f"   ✅ {name}: {response.status_code}")
            else:
                print(f"   ⚠️ {name}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {name}: {e}")

if __name__ == '__main__':
    print("🔧 Probando corrección del error NoReverseMatch...")
    test_url_resolution()
    test_template_rendering()
    print("\n✅ Pruebas completadas!")
