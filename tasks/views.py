#importaciones para loguin y para abrir los views
from django.shortcuts  import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm#para login
from django.contrib.auth.models import User
from django.contrib.auth import login, logout,authenticate
from django.db import IntegrityError
from .forms import  TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required




# Vista para la página de inicio (home)
def home(request):
   # Renderiza la plantilla 'home.html' cuando se accede a la página de inicio
   return render(request, 'home.html')

# Vista para la página de registro (signup)
def signup(request):
    if request.method == 'GET':  # Si la solicitud es GET (cuando el usuario accede a la página de registro)
        # Retorna el formulario de creación de usuario vacío
        # 'UserCreationForm()' es un formulario predeterminado de Django para crear un usuario
        return render(request, 'signup.html', {
            'form': UserCreationForm(),  # Se pasa el formulario vacío al contexto
        })
    else:  # Si la solicitud es POST (cuando el formulario es enviado)
        try:
            # Verifica si las contraseñas introducidas son iguales
            if request.POST['password1'] == request.POST['password2']:
         
                # Intenta crear un nuevo usuario con el nombre de usuario y la contraseña proporcionada
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                
                # Guarda el nuevo usuario en la base de datos
                user.save()
                login(request, user)
                return redirect(task)
        except IntegrityError:
             # Si las contraseñas no coinciden, vuelve a mostrar el formulario con un mensaje de error
            return render(request, 'signup.html', {
                     'form': UserCreationForm,  # Vuelve a mostrar el formulario vacío
                     "error": 'Usuario ya existe'  # Mensaje de error si las contraseñas no coinciden
                })

        # Si las contraseñas no coinciden, vuelve a mostrar el formulario con un mensaje de error
        return render(request, 'signup.html', {
                     'form': UserCreationForm,  # Vuelve a mostrar el formulario vacío
                     "error": 'Las contraseñas no coinciden'  # Mensaje de error si las contraseñas no coinciden
                })

@login_required
def task(request):
    task = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request,'task.html',{'task':task})

@login_required
def task_completed(request):
    task = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'task.html',{'task':task})


@login_required 
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html',{
        'form':TaskForm
        })
    else:
        try:
            form=TaskForm(request.POST)
            new_task =form.save(commit=False)
            new_task.user=request.user
            new_task.save()
            print (new_task)
            return redirect(task)
        except ValueError:
             return render(request, 'create_task.html',{
        'form':TaskForm,
        'error': 'Por favor introduce datos validos'
        })

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task,pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task':task, 'form':form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form=TaskForm(request.POST, instance = task)
            form.save()
            return redirect('task')
        except ValueError:
            return render(request, 'task_detail.html', {'task':task, 'form':form, 'Error': "Error actualizado tarea"})


@login_required
def complete_task(request, task_id):
    task=get_object_or_404(Task, pk=task_id, user=request.user)  
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()  
        return redirect('task')
    
@login_required
def delete_task(request, task_id):
    task=get_object_or_404(Task, pk=task_id, user=request.user)  
    if request.method == 'POST':
        task.delete()  
        return redirect('task')

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('home')



def signin(request):
    # Verifica si la solicitud es de tipo GET
    if request.method == 'GET':
        # Renderiza la plantilla 'signin.html' con el formulario de autenticación
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:  # Si la solicitud es POST (el usuario envió el formulario)
        # Intenta autenticar al usuario con el nombre de usuario y la contraseña enviados
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        
        if user is None:  # Si la autenticación falla (credenciales incorrectas)
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecta'  # Muestra un mensaje de error
            })
        else:  # Si el usuario es válido
            login(request, user)  # Inicia sesión
            return redirect('task')  # Redirige a la vista 'task'

