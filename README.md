# Óptima — Gestor de Proyectos

Aplicación web full stack para la **gestión y seguimiento de proyectos colaborativos**, diseñada para centralizar la administración de proyectos, tareas, integrantes, roles y métricas en una sola plataforma.

Óptima combina un sistema de gestión de tareas con herramientas de seguimiento, colaboración, notificaciones y un asistente inteligente basado en el contexto real de los proyectos.

**Django** · **Django REST Framework** · **Vue 3** · **Vuetify** · **Pinia** · **JWT** · **SQLite**

---

## 📌 About the Project

**Óptima** es una plataforma web de gestión de proyectos colaborativos orientada a equipos que necesitan organizar sus actividades, distribuir responsabilidades y supervisar el avance de sus proyectos desde un único sistema.

La plataforma permite gestionar proyectos y tareas, asignar responsabilidades, controlar permisos según el rol del usuario, consultar métricas de progreso y mantener informados a los integrantes mediante notificaciones dentro de la plataforma y por correo electrónico.

Además, Óptima incorpora un **asistente conversacional con contexto dinámico**, capaz de consultar información relevante del sistema para responder preguntas relacionadas con proyectos, tareas, miembros y métricas.

---

## ✨ Features

### 📁 Gestión de Proyectos

Creación, consulta, actualización y eliminación de proyectos, con información general y seguimiento de su estado.

### 👥 Gestión de Miembros y Roles

Administración de los integrantes de cada proyecto y asignación de roles según las responsabilidades dentro de la plataforma.

### 🔒 Control de Permisos

Los permisos se gestionan de acuerdo con el rol y la relación del usuario con cada proyecto.

El **Project Manager** tiene control sobre la administración de su proyecto, incluyendo acciones como editarlo o eliminarlo, mientras que los demás usuarios tienen acceso a las funcionalidades permitidas según su participación.

### ✅ Gestión de Tareas

Creación y administración de tareas asociadas a proyectos, incluyendo:

* Asignación de responsables.
* Estados de trabajo.
* Prioridades.
* Comentarios.
* Seguimiento del progreso.
* Gestión de tareas según los permisos del usuario.

### 🗂️ Kanban Board

Visualización de tareas mediante un tablero Kanban con movimiento de tareas entre columnas y funcionalidad de **Drag & Drop**.

### 📋 Vista de Lista

Visualización alternativa de las tareas mediante una lista organizada, permitiendo consultar y gestionar grandes cantidades de tareas de manera más sencilla.

### 🔎 Filtros y Búsqueda

Filtrado de tareas por diferentes criterios, facilitando la localización y organización de la información del proyecto.

### 💬 Comentarios en Tareas

Los integrantes pueden utilizar comentarios para colaborar y mantener comunicación relacionada directamente con las tareas.

### 🔔 Notificaciones

Sistema de notificaciones para informar a los usuarios sobre eventos relevantes dentro de la plataforma, incluyendo notificaciones internas y envío de notificaciones por correo electrónico.

### 📊 Dashboard y Métricas

Panel de seguimiento con métricas y visualizaciones para consultar el estado y progreso de los proyectos y sus tareas.

### 🤖 Asistente Inteligente

Chatbot integrado con el sistema capaz de utilizar información dinámica de Óptima para responder consultas relacionadas con:

* Proyectos.
* Tareas.
* Miembros del equipo.
* Métricas y estado general.

El asistente utiliza el contexto real disponible en la plataforma para proporcionar respuestas relacionadas con la información del proyecto.

### 🔐 Autenticación JWT

Sistema de autenticación basado en **JSON Web Tokens (JWT)** para proteger el acceso a la plataforma y sus recursos.

### ✉️ Verificación de Cuenta por Correo

Los usuarios pueden verificar su cuenta mediante un enlace enviado a su correo electrónico.

### 🔑 Restablecimiento de Contraseña

Flujo de recuperación de contraseña mediante correo electrónico, utilizando tokens seguros y validaciones de contraseña proporcionadas por Django.

### 🌙 Modo Claro y Oscuro

Interfaz con soporte para temas claro y oscuro, permitiendo adaptar la experiencia visual de acuerdo con las preferencias del usuario.

---

## 🛠️ Built With

### Backend

* Django
* Django REST Framework
* Python
* JWT Authentication
* Sistema de envío de correo electrónico

### Frontend

* Vue 3
* Vuetify
* Pinia
* Axios

### Database

* SQLite para el entorno de desarrollo
* PostgreSQL previsto para el entorno de despliegue

### AI Integration

* Asistente conversacional integrado mediante API de inteligencia artificial
* Contexto dinámico obtenido de la información de proyectos, tareas, miembros y métricas

---

## 🗄️ Main Data Structure

La plataforma se organiza alrededor de las principales entidades del sistema:

```text
Users
├── Roles
├── Projects
│   ├── Members
│   ├── Tasks
│   │   ├── Status
│   │   ├── Priority
│   │   └── Comments
│   ├── Notifications
│   └── Dashboard Metrics
```

### Users & Roles

Usuarios registrados en la plataforma y roles utilizados para determinar permisos y responsabilidades.

### Projects

Proyectos gestionados dentro de Óptima.

### Project Members

Relación entre usuarios y proyectos, incluyendo el rol que desempeñan dentro de cada proyecto.

### Tasks

Tareas asociadas a proyectos, con información sobre responsables, estados, prioridades y colaboración.

### Comments

Comentarios relacionados con las tareas para facilitar la comunicación entre los integrantes del equipo.

### Notifications

Eventos y avisos generados por diferentes acciones realizadas dentro de la plataforma.

---

## 🔄 How It Works

```text
Register
   ↓
Verify account by email
   ↓
Login with JWT
   ↓
Create or access a project
   ↓
Manage project members and roles
   ↓
Create and assign tasks
   ↓
Manage tasks using Kanban or List View
   ↓
Collaborate through comments
   ↓
Receive platform and email notifications
   ↓
Monitor project metrics through the dashboard
   ↓
Use the AI assistant to query project information
```

Los usuarios pueden gestionar sus proyectos y tareas de acuerdo con los permisos proporcionados por su rol.

El **Project Manager** administra su proyecto y sus configuraciones principales, mientras que los integrantes participan en la ejecución y seguimiento de las tareas asignadas.

---

## 🚀 Getting Started

### Prerequisites

Antes de ejecutar Óptima localmente, asegúrate de tener instalado:

* Python 3.x
* Node.js
* npm
* Git

### 1. Clone the repository

```bash
git clone <URL_DEL_REPOSITORIO>
cd Optima
```

### 2. Backend Setup

Accede al directorio del backend:

```bash
cd backend
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

Configura las variables de entorno necesarias en el archivo `.env`.

Ejemplo de configuración para la URL del frontend:

```env
FRONTEND_URL=http://localhost:5173
```

Ejecuta las migraciones:

```bash
python manage.py migrate
```

Inicia el servidor:

```bash
python manage.py runserver
```

El backend estará disponible normalmente en:

```text
http://127.0.0.1:8000/
```

### 3. Frontend Setup

Accede al directorio del frontend:

```bash
cd frontoptima
```

Instala las dependencias:

```bash
npm install
```

Inicia el servidor de desarrollo:

```bash
npm run dev
```

El frontend estará disponible normalmente en:

```text
http://localhost:5173/
```

---

## 🔐 Authentication Flow

Óptima utiliza autenticación basada en JWT.

El flujo principal es:

```text
Register
   ↓
Email Verification
   ↓
Login
   ↓
JWT Access
   ↓
Authenticated Requests
```

En caso de olvidar la contraseña:

```text
Forgot Password
   ↓
Enter Email
   ↓
Receive Reset Link
   ↓
Open Reset Link
   ↓
Set New Password
   ↓
Login Again
```

---

## 📈 Project Highlights

Óptima busca proporcionar una experiencia de gestión de proyectos centralizada mediante:

* Gestión integral de proyectos y tareas.
* Control de acceso basado en roles.
* Seguimiento visual mediante Kanban.
* Vista alternativa de tareas en formato lista.
* Métricas y visualización del progreso.
* Colaboración mediante comentarios.
* Notificaciones dentro de la plataforma y por correo electrónico.
* Verificación de cuentas y recuperación de contraseñas.
* Asistente inteligente con contexto dinámico del proyecto.

---

## 🔮 Future Improvements

Algunas funcionalidades que pueden considerarse para futuras versiones:

* Invitaciones de usuarios mediante correo electrónico.
* Mejoras adicionales en la experiencia responsive para dispositivos móviles.
* Notificaciones en tiempo real.
* Optimización de la infraestructura para producción.
* Despliegue completo de la plataforma en un entorno cloud.
* Migración del entorno de desarrollo a PostgreSQL para producción.

---

## 📌 Project Status

**Óptima se encuentra en etapa de finalización y preparación para despliegue.**

Las funcionalidades principales de gestión de proyectos, tareas, usuarios, roles, permisos, colaboración, notificaciones, métricas y asistente inteligente se encuentran implementadas.

La siguiente etapa se enfoca en la estabilización final, migración de la base de datos y despliegue de la plataforma.
