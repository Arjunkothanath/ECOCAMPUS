from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from general.models import Feedback, Bin
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils import timezone


User = get_user_model() 

@login_required
def headstaff_dashboard(request):
    print(request.user.role)
    if request.user.role.strip().lower() == 'headstaff':

        staff_count = User.objects.filter(role='staff').count()
        feedback_count = Feedback.objects.filter(user__role__in=['student', 'staff']).count()
        resolved_count = Feedback.objects.filter(status='Resolved').count()
        pending_count = Feedback.objects.filter(status='Pending').count()

        context = {
            'staff_count': staff_count,
            'feedback_count': feedback_count,
            'resolved_count': resolved_count,
            'pending_count': pending_count,
        }
    else:
        return render(request, '403.html')

    return render(request, 'headstaff/headstaff_dashboard.html', context)
 # This will use your custom User model

@login_required
def add_staff_by_head(request):
    if request.user.role != 'headstaff':
        return render(request, '403.html')

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        if role not in ['staff']:
            return render(request, 'add_staff.html', {'error': 'Only staff allowed'})

        if User.objects.filter(username=username).exists():
            return render(request, 'add_staff.html', {'error': 'Username already exists'})

        User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            role=role
        )
        return redirect('headstaff_dashboard')

    return render(request, 'add_staff.html')


@login_required
def view_feedback_by_headstaff(request):
    if request.user.role != 'headstaff':
        return render(request, '403.html')

    feedbacks_from_students_staff = Feedback.objects.filter(
        user__role__in=['student', 'staff']
    ).order_by('-created_at')

    own_feedbacks = Feedback.objects.filter(user=request.user).order_by('-created_at')
    bins = Bin.objects.all()

    return render(request, 'headstaff/feedback.html', {
        'feedbacks': feedbacks_from_students_staff,
        'own_feedbacks': own_feedbacks,
        'bins': bins
    })



@login_required
def view_users_by_headstaff(request):
    if request.user.role != 'headstaff':
        return render(request, '403.html')

    filter_role = request.GET.get('role')  # ?role=student or staff
    if filter_role in ['student', 'staff']:
        users = User.objects.filter(role=filter_role).order_by('username')
    else:
        users = User.objects.filter(role__in=['student', 'staff']).order_by('role', 'username')

    return render(request, 'headstaff/view_users.html', {
        'users': users,
        'filter_role': filter_role,
    })

@login_required
def manage_staff(request):
    if request.user.role != 'headstaff':
        return render(request, '403.html')

    staff_users = User.objects.filter(role='staff')

    return render(request, 'headstaff/manage_staff.html', {'staff_users': staff_users})

@login_required
def edit_staff(request, user_id):
    if request.user.role != 'headstaff':
        return render(request, '403.html')

    staff = get_object_or_404(User, id=user_id, role='staff')

    if request.method == 'POST':
        staff.username = request.POST.get('username')
        staff.email = request.POST.get('email')
        staff.save()
        return redirect('manage_staff')

    return render(request, 'headstaff/edit_staff.html', {'staff': staff})

@login_required
def delete_staff(request, user_id):
    if request.user.role != 'headstaff':
        return render(request, '403.html')

    staff = get_object_or_404(User, id=user_id, role='staff')
    staff.delete()
    return redirect('manage_staff')

@login_required
def submit_feedback_headstaff(request):
    if request.user.role != 'headstaff':
        return render(request, '403.html')

    if request.method == 'POST':
        feedback_type = request.POST.get('type')
        location = request.POST.get('location')
        other_location = request.POST.get('other_location')
        message = request.POST.get('message')

        final_location = other_location if location == 'Others' else location

        Feedback.objects.create(
            user=request.user,
            feedback_type=feedback_type,
            location=final_location,
            message=message,
            status="Pending" if feedback_type == "Alert" else "Unread",
            created_at=timezone.now()
        )

        messages.success(request, "Feedback submitted successfully.")
        return redirect('headstaff_dashboard')

    return render(request, 'headstaff/headstaff_submit_feedback.html')