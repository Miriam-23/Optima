# Optima — Backend

API REST desarrollada con Django y Django REST Framework.

## Requisitos
- Python 3.10+
- pip

## Instalación

1. Crear entorno virtual:
   python -m venv venv

2. Activar entorno virtual:
   - Windows: venv\Scripts\activate
   - Mac/Linux: source venv/bin/activate

3. Instalar dependencias:
   pip install -r requirements.txt

4. Correr migraciones:
   python manage.py migrate

5. Crear superusuario (para acceder al admin):
   python manage.py createsuperuser

6. Levantar el servidor:
   python manage.py runserver

## Endpoints
Ver API_Contract_Optima_v1.1.docx para la documentación completa.