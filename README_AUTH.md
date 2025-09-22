# Implementación de Autenticación en Malla Universitaria

Este documento explica cómo implementar la autenticación de Django en el proyecto Malla Universitaria.

## Archivos Creados/Modificados

### 1. Templates de Autenticación
- `maya_uni/malla/templates/malla/login.html` - Página de inicio de sesión
- `maya_uni/malla/templates/malla/base_auth.html` - Template base con autenticación

### 2. Vistas con Autenticación
- `maya_uni/malla/views_auth.py` - Vistas con decoradores @login_required

### 3. URLs con Autenticación
- `maya_uni/malla/urls_auth.py` - URLs que usan las vistas autenticadas
- `maya_uni/maya_uni/urls_auth.py` - URLs principales del proyecto con autenticación

## Configuración de Django

La configuración de autenticación ya está habilitada en `settings.py`:
- `django.contrib.auth` está en INSTALLED_APPS
- `AuthenticationMiddleware` está en MIDDLEWARE
- `auth` context processor está en TEMPLATES

## Para Implementar la Autenticación

### 1. Crear un Superusuario
```bash
cd maya_uni
python manage.py createsuperuser
```

### 2. Usar las URLs de Autenticación
Reemplaza en tu proyecto principal:
- `maya_uni/urls.py` → `maya_uni/maya_uni/urls_auth.py`
- `malla/urls.py` → `malla/urls_auth.py`
- `malla/views.py` → `malla/views_auth.py`
- `malla/templates/malla/base.html` → `malla/templates/malla/base_auth.html`

### 3. Funcionalidades Implementadas

#### Decoradores de Autenticación
Todas las vistas principales ahora requieren autenticación:
- `@login_required` en todas las vistas
- Redirección automática a login si no está autenticado

#### Template Base con Autenticación
- Muestra nombre de usuario cuando está logueado
- Botón de "Cerrar Sesión" para usuarios autenticados
- Botón de "Iniciar Sesión" para usuarios no autenticados
- Oculta el menú si no está autenticado

#### Página de Login
- Formulario de login con estilo Bootstrap
- Manejo de errores de autenticación
- Enlaces para recuperación de contraseña (si se configura)

## Flujo de Autenticación

1. **Usuario no autenticado**: Ve la página de login
2. **Login exitoso**: Redirige a `/malla/semesters/`
3. **Usuario autenticado**: Puede acceder a todas las funcionalidades
4. **Logout**: Redirige a la página de login

## Configuración Adicional (Opcional)

### Para agregar recuperación de contraseña:
1. Agregar a `maya_uni/maya_uni/urls_auth.py`:
```python
path('password-reset/', auth_views.PasswordResetView.as_view(template_name='malla/password_reset.html'), name='password_reset'),
path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='malla/password_reset_done.html'), name='password_reset_done'),
```

### Para personalizar más la autenticación:
- Modificar `LOGIN_REDIRECT_URL` en settings.py
- Crear templates personalizados para password reset
- Agregar registro de usuarios si es necesario

## Seguridad

- Todas las vistas sensibles requieren autenticación
- CSRF protection habilitado
- Secure password validation
- Session management automático de Django

## Pruebas

Para probar la implementación:

1. Inicia el servidor: `python manage.py runserver`
2. Ve a cualquier página (ej: `/malla/semesters/`)
3. Deberías ser redirigido a `/login/`
4. Crea un superusuario y prueba el login
5. Después del login deberías poder acceder a todas las páginas
