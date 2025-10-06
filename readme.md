# Campus online – Gestor de Perfiles Estudiantiles (Django)

App web en **Django** para gestionar **perfiles de estudiantes**.

Incluye **inicio con login embebido**, **detalle de perfil** con control de acceso y **logout seguro**.

## Características

- **Home con login** (sin sesión muestra el formulario; con sesión redirige al perfil).
- **Perfil relacionado 1 a 1 con User y modelo**: cada usuario posee una entrada en el modelo `PerfilEstudiante`.
- **Auto-creación de perfil** vía **signals** al crear usuarios.
- **Privacidad y autorización**: solo el dueño ve su propio perfil.

---

## Tecnologías

- Python 3.10+ (probado en 3.13)
- Django 5.x
- SQLite (para desarrollo)

---

## Estructura

```
campus/
├─ manage.py
├─ campus/
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
├─ perfiles/
│  ├─ apps.py
│  ├─ models.py
│  ├─ signals.py
│  ├─ views.py
│  └─ templates/
│     └─ perfiles/
│        └─ perfil_detalle.html
└─ templates/
   ├─ base.html
   └─ inicio.html

```

---

## Puesta en marcha

### 1) Clonar y entorno

```bash
git clone <URL_DEL_REPO>
cd campus
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
pip install -r requirements.txt  # si existe; si no, pip install django

```

> Si no se encuentra requirements.txt, se puede instalar Django:
> 

```bash
pip install "Django>=5,<6"

```

### 2) Configuración mínima

En `campus/settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
    'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
    'perfiles.apps.PerfilesConfig',  # importante: clase de la app
]

TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']
LOGIN_REDIRECT_URL = 'inicio'
LOGOUT_REDIRECT_URL = 'inicio'

```

### 3) Migraciones y superusuario

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

```

### 4) Ejecutar

```bash
python manage.py runserver

```

### URLs para pruebas en desarrollo

- Home: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

---

### Templates

- `templates/base.html`: layout con logout por **POST**.
- `templates/inicio.html`: login o selector para vincular perfil.
- `perfiles/templates/perfiles/perfil_detalle.html`: detalle de perfil.

> Anotacion para Django 5: El LogoutView no acepta GET. Usar formulario con method="post" y {% csrf_token %}.
> 

---

## Flujo de uso

1. **Sin sesión** → Home muestra **login**.
2. **Login OK** → redirige a **inicio**:
    - Si hay perfil asociado → **redirige** a `/perfil/<pk>/`.
    - Si no hay perfil → muestra **selector** de perfiles sin dueño para **vincular**.
3. **Detalle de perfil** → solo el dueño puede verlo.
4. **Logout (POST)** → vuelve a Home con login.

---

## Pruebas manuales (checklist)

- [ ]  Login desde `/` → redirige a tu perfil.
- [ ]  Acceso directo a `/perfil/<otro_pk>/` → redirige a `/`.
- [ ]  Usuario sin perfil → puede vincular uno sin dueño.
- [ ]  Logout por POST → vuelve a `/`.
- [ ]  Admin crea usuario → perfil se crea automáticamente por signal.

---

## Solución a errores comunes

- **TemplateDoesNotExist (`inicio.html`)**
    
    Se asegura que `templates/` esté en el **nivel de `manage.py`** y que `TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']`.
    
- **Application labels aren't unique (duplicates: perfiles)**
    
    En `INSTALLED_APPS` dejar **solo** `'perfiles.apps.PerfilesConfig'` (`'perfiles'` se mantuvo pero se comentó).
    
- **ImportError: cannot import name 'perfil_detalle'**
    
    Se verifica que la función exista en `perfiles/views.py` y en `urls.py` usa `from perfiles import views`.
    
- **TemplateDoesNotExist (`perfiles/perfil_detalle.html`)**
    
    Se puso el archivo en `perfiles/templates/perfiles/perfil_detalle.html`.
    
- **403 CSRF token incorrect**
    
    Recarga la home (GET) y envía nuevamente el formulario; evita reintentar el POST desde “Atrás”.
    
- **405 Method Not Allowed en logout**
    
    Se paso a usar **formulario POST** al `LogoutView` (ya que Django 5 no acepta GET).
    

---

## Roadmap

- [ ]  **Editar mi perfil** (form de actualización + permisos).
- [ ]  **Mensajes flash** (`django.contrib.messages`) para feedback UX.
- [ ]  **Vistas 403/404 personalizadas**.
- [ ]  Integración de  **API restful**