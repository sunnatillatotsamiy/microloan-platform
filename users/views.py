from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User


def home_view(request):
    return render(request, 'home.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already taken'})
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('/dashboard/')
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


@login_required
def user_list_view(request):
    if request.user.role != 'manager':
        return redirect('/dashboard/')
    users = User.objects.all().order_by('date_joined')
    return render(request, 'user_list.html', {'users': users})


@login_required
def user_create_view(request):
    if request.user.role != 'manager':
        return redirect('/dashboard/')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        if User.objects.filter(username=username).exists():
            return render(request, 'user_form.html', {'error': 'Username already taken', 'action': 'Create'})
        User.objects.create_user(username=username, email=email, password=password, role=role)
        messages.success(request, f'User {username} created successfully.')
        return redirect('/users/')
    return render(request, 'user_form.html', {'action': 'Create'})


@login_required
def user_edit_view(request, user_id):
    if request.user.role != 'manager':
        return redirect('/dashboard/')
    target_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        target_user.username = request.POST['username']
        target_user.email = request.POST['email']
        target_user.role = request.POST['role']
        target_user.phone_number = request.POST.get('phone_number', '')
        new_password = request.POST.get('password', '').strip()
        if new_password:
            target_user.set_password(new_password)
        target_user.save()
        messages.success(request, f'User {target_user.username} updated successfully.')
        return redirect('/users/')
    return render(request, 'user_form.html', {'action': 'Edit', 'target_user': target_user})


@login_required
def user_delete_view(request, user_id):
    if request.user.role != 'manager':
        return redirect('/dashboard/')
    target_user = get_object_or_404(User, id=user_id)
    if request.user.id == target_user.id:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('/users/')
    if request.method == 'POST':
        username = target_user.username
        target_user.delete()
        messages.success(request, f'User {username} deleted successfully.')
        return redirect('/users/')
    return render(request, 'user_confirm_delete.html', {'target_user': target_user})
