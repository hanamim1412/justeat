from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, LoginForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Restaurant, Customer, Rider


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'User created successfully. Please log in.')
            return redirect('login_view')
        else:
            messages.error(request, 'Form is not valid. Please correct the errors below.')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)
    next_url = request.GET.get('next')
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_customer:
                    redirect(next_url) if next_url else redirect('customer')
                    return redirect('index')
                elif user.is_restaurant:
                    return redirect('restaurant')
                elif user.is_rider:
                    return redirect('rider')
                elif user.is_superuser:
                    return redirect('dashboard')
            else:
                messages.error(request, 'Invalid credentials')
            
        else:
            form = SignUpForm()     
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

