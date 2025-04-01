from django.db import models  # Importa el módulo de modelos de Django
from django.contrib.auth.models import User  # Importa el modelo de usuario de Django

# Modelo de la tabla Task (Tareas)
class Task(models.Model):
    title = models.CharField(max_length=100)  # Campo de texto con un máximo de 100 caracteres para el título
    
    description = models.TextField(blank=True)  # Campo de texto largo opcional (puede estar vacío)
    
    created = models.DateTimeField(auto_now_add=True)  
    # Almacena la fecha y hora de creación automáticamente al guardar la tarea
    
    datecompleted = models.DateTimeField(null=True, blank=True)  
    # Fecha de finalización de la tarea, opcional (puede estar vacía)
    
    important = models.BooleanField(default=False)  
    # Indica si la tarea es importante, por defecto es False
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    # Relación con el modelo User, cada tarea pertenece a un usuario
    # Si el usuario se elimina, también se eliminan sus tareas (on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - by ' + self.user.username  
    # Representación en texto del modelo, muestra el título de la tarea y el usuario que la creó
