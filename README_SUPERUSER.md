# Protección de Superusuario para Crear Semestre

Este documento explica cómo implementar la protección de superusuario para la vista de crear semestre.

## Archivos Creados/Modificados

### 1. Decorador Personalizado
- `maya_uni/malla/decorators.py` - Decorador `@superuser_required` personalizado

### 2. Vista de Administrador
- `maya_uni/malla/views_admin_final.py` - Vista `create_semester` con protección de superusuario

### 3. URLs de Administrador
- `maya_uni/malla/urls_admin.py` - URLs que usan la vista de administrador

### 4. Templates
- `maya_uni/malla/templates/malla/base_admin.html` - Template base con control de permisos
- `maya_uni/malla/templates/malla/create_semester_admin.html` - Template específico para crear semestre (admin)

## Funcionalidades Implementadas

### Decorador `@superuser_required`
```python
@superuser_required
def create_semester(request):
    # Solo superusuarios pueden acceder
```

**Comportamiento:**
- ✅ **Superusuarios**: Acceso completo
- ❌ **Usuarios normales**: Redirección a lista de semestres con mensaje de error
- 📝 **No autenticados**: Redirección a login

### Template Base con Control de Permisos
```html
{% if user.is_superuser %}
<li class="nav-item mb-2">
    <a class="nav-link" href="{% url 'malla:create_semester' %}">
        <i class="bi bi-plus-circle me-2"></i>Crear Semestre
    </a>
</li>
{% endif %}
```

**Características:**
- 🔒 Oculta el enlace "Crear Semestre" para usuarios no administradores
- 🏷️ Muestra badge "Admin" para superusuarios
- 🎨 Diseño visual diferenciado para administradores

### Template de Crear Semestre (Admin)
- 🛡️ Interfaz específica para administradores
- ⚠️ Indicadores visuales de que es una función restringida
- 📋 Mejor manejo de errores y mensajes

## Para Implementar la Protección

### 1. Reemplazar Archivos
```bash
# Reemplazar las URLs
cp maya_uni/malla/urls_admin.py maya_uni/malla/urls.py

# Reemplazar las vistas
cp maya_uni/malla/views_admin_final.py maya_uni/malla/views.py

# Reemplazar el template base
cp maya_uni/malla/templates/malla/base_admin.html maya_uni/malla/templates/malla/base.html
```

### 2. Crear Superusuario
```bash
cd maya_uni
python create_superuser.py
```

### 3. Probar la Protección

#### Como Superusuario:
- ✅ Puede ver el enlace "Crear Semestre" en el menú
- ✅ Puede acceder directamente a `/malla/semesters/create/`
- ✅ Puede crear semestres normalmente

#### Como Usuario Normal:
- ❌ No ve el enlace "Crear Semestre" en el menú
- ❌ Si intenta acceder directamente, es redirigido con mensaje de error
- ✅ Puede acceder a todas las demás funcionalidades

## Mensajes de Error

### Para Usuarios No Autorizados:
```
"Solo los administradores pueden acceder a esta página."
```

### Para Superusuarios Exitosos:
```
"Semestre creado exitosamente."
```

## Seguridad Implementada

1. **Control de Acceso**: Solo superusuarios pueden crear semestres
2. **Ocultación de UI**: El enlace no aparece para usuarios normales
3. **Redirección Segura**: No autenticados van a login, normales van a lista
4. **Mensajes Informativos**: Feedback claro sobre permisos

## Pruebas Recomendadas

1. **Login como admin**:
   ```bash
   Usuario: admin
   Contraseña: admin123
   ```

2. **Verificar menú**: Debe aparecer "Crear Semestre"

3. **Crear semestre**: Debe funcionar normalmente

4. **Logout y login como usuario normal**:
   - No debe aparecer el enlace
   - Acceso directo debe redirigir con error

5. **Probar acceso directo**: `/malla/semesters/create/` debe redirigir

## Configuración Adicional

### Para agregar más vistas de administrador:
```python
from .decorators import superuser_required

@superuser_required
def otra_vista_admin(request):
    # Solo superusuarios
    pass
```

### Para personalizar mensajes:
```python
# En decorators.py
messages.error(request, 'Mensaje personalizado de error.')
```

## Compatibilidad

- ✅ Compatible con autenticación existente
- ✅ No afecta otras funcionalidades
- ✅ Mantiene todos los estilos Bootstrap
- ✅ Funciona con el sistema de mensajes de Django
