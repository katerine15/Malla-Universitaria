#!/usr/bin/env python
"""
Script para probar la protección de superusuario
Ejecutar: python test_superuser.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maya_uni.settings')
django.setup()

from django.test import Client, RequestFactory
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from malla.decorators import superuser_required

def test_superuser_protection():
    """Probar la protección de superusuario"""
    print("🧪 Probando protección de superusuario...")

    # Crear usuarios de prueba
    admin_user = User.objects.create_superuser('admin_test', 'admin@test.com', 'admin123')
    normal_user = User.objects.create_user('user_test', 'user@test.com', 'user123')

    # Crear cliente de prueba
    client = Client()

    # Probar acceso como usuario normal
    print("\n1️⃣ Probando acceso como usuario normal...")
    client.login(username='user_test', password='user123')

    response = client.get('/malla/semesters/create/', follow=True)
    print(f"   Status Code: {response.status_code}")

    # Verificar redirección
    if response.redirect_chain:
        print(f"   ✅ Redirigido correctamente a: {response.redirect_chain[0][0]}")

        # Verificar mensaje de error
        messages = list(get_messages(response.wsgi_request))
        if messages:
            print(f"   ✅ Mensaje de error: {messages[0].message}")
        else:
            print("   ⚠️ No se encontró mensaje de error")
    else:
        print("   ❌ No se redirigió correctamente")

    # Cerrar sesión
    client.logout()

    # Probar acceso como superusuario
    print("\n2️⃣ Probando acceso como superusuario...")
    client.login(username='admin_test', password='admin123')

    response = client.get('/malla/semesters/create/')
    print(f"   Status Code: {response.status_code}")

    if response.status_code == 200:
        print("   ✅ Superusuario puede acceder correctamente")
    else:
        print("   ❌ Superusuario no puede acceder")

    # Cerrar sesión
    client.logout()

    # Probar acceso sin autenticación
    print("\n3️⃣ Probando acceso sin autenticación...")
    response = client.get('/malla/semesters/create/', follow=True)
    print(f"   Status Code: {response.status_code}")

    if 'login' in response.redirect_chain[0][0]:
        print("   ✅ No autenticado redirigido a login correctamente")
    else:
        print("   ❌ No autenticado no redirigido correctamente")

    # Limpiar usuarios de prueba
    admin_user.delete()
    normal_user.delete()

    print("\n✅ Pruebas completadas!")

if __name__ == '__main__':
    test_superuser_protection()
