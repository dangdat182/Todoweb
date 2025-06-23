from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Task, User
from datetime import datetime
import json
import os
from django.conf import settings
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# Create your views here.

# Home View
def home(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    return render(request, 'tasks/home.html')

# User Registration View
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'tasks/register.html')
        
        if User.objects.filter(username=username).first():
            messages.error(request, 'Username already exists.')
            return render(request, 'tasks/register.html')
        if User.objects.filter(email=email).first():
            messages.error(request, 'Email already registered.')
            return render(request, 'tasks/register.html')
        
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'tasks/register.html')
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password1)
        user.save()
        
        # Log the user in
        request.session['user_id'] = str(user.id)
        messages.success(request, 'Account created successfully!')
        return redirect('task_list')
    
    return render(request, 'tasks/register.html')

# Custom login view
def custom_login(request):
    if request.method == 'POST':
        login_input = request.POST.get('username')
        password = request.POST.get('password')
        
        # Try to find user by username or email
        user = User.objects.filter(username=login_input).first()
        if not user:
            user = User.objects.filter(email=login_input).first()
        if user and user.check_password(password):
            request.session['user_id'] = str(user.id)
            return redirect('task_list')
        else:
            messages.error(request, 'Invalid username/email or password.')
    
    return render(request, 'tasks/login.html')

# Custom logout view
def custom_logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('home')

# Custom authentication middleware
def get_current_user(request):
    if 'user_id' in request.session:
        try:
            return User.objects.get(id=request.session['user_id'])
        except User.DoesNotExist:
            del request.session['user_id']
    return None

# Task List View
def task_list(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')
    
    tasks = Task.objects.filter(user=user)
    shared_tasks = Task.objects.filter(shared_with=user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'shared_tasks': shared_tasks, 'user': user})

# Create Task View
def create_task(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            task = Task(
                title=data['title'],
                description=data.get('description', ''),
                due_date=datetime.fromisoformat(data['due_date'].replace('Z', '+00:00')) if data.get('due_date') else None,
                user=user
            )
            task.save()
            return JsonResponse({
                'success': True,
                'task': {
                    'id': str(task.id),
                    'title': task.title,
                    'description': task.description,
                    'due_date': task.due_date.isoformat() if task.due_date else None,
                    'completed': task.completed
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return render(request, 'tasks/create_task.html')

# Update Task View
def update_task(request, task_id):
    user = get_current_user(request)
    if not user:
        return redirect('login')
    
    try:
        task = Task.objects.get(id=task_id, user=user)
        if request.method == 'POST':
            data = json.loads(request.body)
            task.title = data['title']
            task.description = data.get('description', '')
            if data.get('due_date'):
                task.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
            task.save()
            return JsonResponse({
                'success': True,
                'task': {
                    'id': str(task.id),
                    'title': task.title,
                    'description': task.description,
                    'due_date': task.due_date.isoformat() if task.due_date else None,
                    'completed': task.completed
                }
            })
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    except Task.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task not found'})

# Delete Task View
def delete_task(request, task_id):
    user = get_current_user(request)
    if not user:
        return redirect('login')
    
    try:
        task = Task.objects.get(id=task_id, user=user)
        task.delete()
        return JsonResponse({'success': True})
    except Task.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task not found'})

# Toggle Task Completion View
def toggle_task(request, task_id):
    user = get_current_user(request)
    if not user:
        return redirect('login')
    
    try:
        task = Task.objects.get(id=task_id, user=user)
        task.completed = not task.completed
        task.save()
        return JsonResponse({'success': True, 'completed': task.completed})
    except Task.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task not found'})

def google_login(request):
    flow = Flow.from_client_secrets_file(
        os.path.join(settings.BASE_DIR, 'client_secret.json'),
        scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
        redirect_uri=request.build_absolute_uri('/oauth2callback/')
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    request.session['oauth_state'] = state
    return redirect(authorization_url)

def oauth2callback(request):
    state = request.session.get('oauth_state')
    flow = Flow.from_client_secrets_file(
        os.path.join(settings.BASE_DIR, 'client_secret.json'),
        scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
        state=state,
        redirect_uri=request.build_absolute_uri('/oauth2callback/')
    )
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials
    idinfo = id_token.verify_oauth2_token(
        credentials._id_token,
        google_requests.Request(),
        audience=flow.client_config['client_id']
    )
    email = idinfo.get('email')
    username = email.split('@')[0]
    from .models import User
    user = User.objects(email=email).first()
    if not user:
        user = User(username=username, email=email)
        user.set_password(os.urandom(16).hex())  # random password
        user.save()
    request.session['user_id'] = str(user.id)
    return redirect('task_list')

def account(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')
    return render(request, 'tasks/account.html', {'user': user})

# Share Task View
def share_task(request, task_id):
    user = get_current_user(request)
    if not user:
        return redirect('login')
    
    try:
        task = Task.objects.get(id=task_id, user=user)
        if request.method == 'POST':
            data = json.loads(request.body)
            share_with_username = data.get('username')
            share_with_user = User.objects(username=share_with_username).first()
            if not share_with_user:
                return JsonResponse({'success': False, 'error': 'User not found'})
            if share_with_user not in task.shared_with:
                task.shared_with.append(share_with_user)
                task.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    except Task.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task not found'})

# List tasks shared with the user
@login_required
def shared_tasks(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')
    tasks = Task.objects.filter(shared_with=user)
    return render(request, 'tasks/shared_tasks.html', {'tasks': tasks, 'user': user})
