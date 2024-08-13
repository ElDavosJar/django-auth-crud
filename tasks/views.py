from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    #check if the request is a GET request or a POST request
    if request.method == 'GET':
        return render(request, 'signup.html', {
        'form': UserCreationForm
        })
    else:
        #check if the password entered by the user matches
        if request.POST['password1'] == request.POST['password2']:
            #check if the username entered by the user is unique
            try:
                #create a new user with the username and password entered by the user
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            #if the username is not unique, return an error message
            except IntegrityError:
                return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'username already taken'
            })
        #if the passwords do not match, return an error message
        return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'Passwords did not match'
            })
        
@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {
        'tasks': tasks
    })
    
@login_required
def completed_tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted') 
    return render(request, 'tasks.html', {
        'tasks': tasks
    })
    
@login_required
def create_task(request):
    
    if request.method =='GET':
        return render(request, 'create_task.html',{
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            print(new_task)
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Bad data passed in. Try again.'
            })
            
@login_required
def task_detail(request, task_pk):
    if request.method == 'GET':
        #serch for the task in the database & check if the task belongs to the user
        task = get_object_or_404(Task, pk=task_pk, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_details.html',{ 
            'task': task,
            'form': form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_pk)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_details.html', {
                'task': task,
                'form': form,
                'error': 'Bad data passed in. Try again.'
            })
            
@login_required
def complete_task(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
    
@login_required
def delete_task(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def signout(request):
    logout(request)
    return render(request, 'home.html')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
        'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST
            ['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'username and password did not match'
            })
        else:
            login(request, user)
            return redirect('tasks')
    
