from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .models import Feedback


User = get_user_model()

def home(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'email already exists'})

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            role='student'
        )
        return redirect('login_view')

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            print("Logged in as:", user.username, "| Role:", user.role)  # ✅ Add this
            role = user.role.strip().lower()  # Clean it once

            if role == 'admin':
                print("Redirecting to corporate dashboard...")
                return redirect('admin_dashboard')
            elif role == 'corporate':
                print("Redirecting to corporate dashboard...")
                return redirect('corporate_dashboard')
            elif role == 'headstaff':
                print("Redirecting to headstaff dashboard...")
                return redirect('headstaff_dashboard')
            elif role == 'staff':
                print("Redirecting to headstaff dashboard...")
                return redirect('staff_dashboard')
            elif role == 'student':
                print("Redirecting to headstaff dashboard...")
                return redirect('student_dashboard')
            else:
                return render(request, '403.html')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


@login_required
def submit_feedback(request):
    if request.method == 'POST':
        location = request.POST['location']
        message = request.POST['message']
        Feedback.objects.create(user=request.user, location=location, message=message)
        return render(request, 'feedback_success.html')

    return render(request, 'submit_feedback.html')


def logout_view(request):
    logout(request)
    return redirect('login_view')

def about_page(request):
    return render(request, 'about.html')

def contact_page(request):
    return render(request, 'contact.html')


