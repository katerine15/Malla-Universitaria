#!/usr/bin/env python
"""
Script para crear un superusuario automáticamente para pruebas de autenticación.
Ejecutar: python create_superuser.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maya_uni.settings')
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    """Crear un superusuario para pruebas"""
    username = 'admin'
    email = 'admin@example.com'
    password = 'admin123'

    # Verificar si el usuario ya existe
    if User.objects.filter(username=username).exists():
        print(f"✓ El superusuario '{username}' ya existe.")
        return

    # Crear el superusuario
    try:
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print("✓ Superusuario creado exitosamente!")
        print(f"   Usuario: {username}")
        print(f"   Email: {email}")
        print(f"   Contraseña: {password}")
        print("\nPuedes iniciar sesión en: http://localhost:8000/login/")
    except Exception as e:
        print(f"✗ Error al crear superusuario: {e}")
        sys.exit(1)

if __name__ == '__main__':
    create_superuser()
