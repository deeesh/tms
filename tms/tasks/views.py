from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import TaskForm, TaskUpdateForm, CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from .models import Task
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken




def loginUser(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return redirect("/dashboard", {'access_token':access_token})
    return render(request, 'login.html')


def userRegister(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form':form})


@login_required
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required
def dashboardView(request):
    if request.user.is_anonymous:
        return redirect("/login")
    task_list = Task.objects.all().order_by('created_at')
    tasks_per_page = 5
    paginator = Paginator(task_list, tasks_per_page)
    page = request.GET.get('page')
    try:
        task_list = paginator.page(page)
    except PageNotAnInteger:
        task_list = paginator.page(1)
    except EmptyPage:
        task_list = paginator.page(paginator.num_pages)
    
    return render(request, 'index.html', {'task_list':task_list})


@login_required
def viewTaskDescription(request, task_id):
    if request.user.has_perm('tasks.can_view_task_description') or request.user.is_superuser:
        task = Task.objects.get(id = task_id)
    else:
        return render(request, 'error_403.html')
    return render(request, 'task_description.html', {'task': task})


@login_required
def createTask(request):
    if request.user.has_perm('tasks.can_update_task') or request.user.is_superuser:
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.completed = False 
                task.save()
                return redirect('/dashboard')
        else:
            form = TaskForm()
    else:
        return render(request, 'error_403.html')
    return render(request, 'create_task.html', {'form': form})


@login_required
def updateTask(request, task_id):
    task = Task.objects.get(id = task_id)

    if request.user.has_perm('tasks.can_update_task') or request.user.is_superuser:
        if request.method == 'POST':
            form = TaskUpdateForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect('/dashboard')
        else:
            form = TaskUpdateForm(instance=task)
    else:
        return render(request, 'error_403.html')
    return render(request, 'update_task.html', {'form': form, 'task': task})


@login_required
def markTaskCompleted(request, task_id):
    task = Task.objects.get(id = task_id)
    if request.user.has_perm('tasks.can_mark_complete') or request.user.is_superuser:
        if request.method == 'POST':
            if 'completed' in request.POST:
                task.completed = not task.completed
                task.save()
                messages.success(request, 'Task marked as complete.')
    else:
        return render(request, 'error_403.html')
    return redirect('/dashboard')