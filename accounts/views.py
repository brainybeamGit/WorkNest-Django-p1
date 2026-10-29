from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not email or not phone or not password or not confirm_password:
            messages.error(request, 'Please fill in all fields.')

        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')

        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')

        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')

        elif len(password) < 8:
            messages.error(request, 'Password must contain at least 8 characters.')

        else:
             new_user = User.objects.create_user(
                  username=username,
                  email=email,
                  password=password
                  )
             Profile.objects.create(
                 user=new_user,
                 phone=phone
                 )
             messages.success(request, 'Registration successful! Please log in.')
             return redirect('login')

    return render(request, 'accounts/register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')

            next_url = request.POST.get('next') or request.GET.get('next')

            if next_url and next_url.startswith('/') and not next_url.startswith('//'):
                return redirect(next_url)

            return redirect('home')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')

@login_required
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have logged out successfully.')
        return redirect('login')

    return redirect('home')