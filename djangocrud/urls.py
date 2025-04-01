"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Ejemplos:
Vistas de funciones
1. Agregar una importación: from my_app import views
2. Agregar una URL a urlpatterns: path('', views.home, name='home')
Vistas basadas en clases
1. Agregar una importación: from other_app.views import Home
2. Agregar una URL a urlpatterns: path('', Home.as_view(), name='home')
Inclusión de otra URLconf
1. Importar la función include(): from django.urls import include, path
2. Agregar una URL a urlpatterns: path('blog/', include('blog.urls'))
"""
from django.contrib import admin  # Importa el módulo de administración de Django
from django.urls import path  # Importa la función 'path' para definir rutas
from tasks import views  # Importa las vistas desde la aplicación 'tasks'

# Definición de las rutas del proyecto
urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para acceder al panel de administración de Django
    
    path('', views.home, name='home'),  # Ruta de la página de inicio
    
    path('signup/', views.signup, name='signup'),  # Ruta para el registro de usuarios

    path('task/create/', views.create_task, name='create_task'),  # Ruta para crear una nueva tarea

    path('task/', views.task, name='task'),  # Ruta para visualizar las tareas

    path('task_completed', views.task_completed, name='task_completed'),  # Ruta para visualizar las tareas cpmpletadas
    
    path('task/<int:task_id>/', views.task_detail, name='task_detail') , 
    # Ruta dinámica que recibe un ID de tarea y muestra sus detalles

    path('task/<int:task_id>/complete', views.complete_task, name='complete_task') ,

     path('task/<int:task_id>/Delete', views.delete_task, name='delete_task') ,
    
    path('logout/', views.cerrar_sesion, name='logout'),  # Ruta para cerrar sesión
    
    path('signin/', views.signin, name='signin')  # Ruta para iniciar sesión
    
    
    
]
