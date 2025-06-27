from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from general.models import Bin, BinCollection
from django.shortcuts import get_object_or_404
from general.models import Feedback
from django.db.models import Case, When, IntegerField
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


User = get_user_model()

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return render(request, '403.html')
    total_bins = Bin.objects.count()
    full_bins = Bin.objects.filter(status='Full').count()
    empty_bins = Bin.objects.filter(status='Empty').count()
    total_feedbacks = Feedback.objects.count()

    context = {
        'total_bins': total_bins,
        'full_bins': full_bins,
        'empty_bins': empty_bins,
        'total_feedbacks': total_feedbacks,
    }
    return render(request, 'dashboard.html', context)

@login_required
def view_users(request):
    if request.user.role != 'admin':
        return render(request, '403.html')

    role = request.GET.get('role')  # Get filter from URL if any
    if role:
        users = User.objects.filter(role=role)
    else:
        users = User.objects.all().exclude(role='admin')
    
    return render(request, 'view_users.html', {'users': users, 'selected_role': role})

@login_required
def add_user(request):
    if request.user.role != 'admin':
        return render(request, '403.html')  # Only admin allowed

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        if role not in ['staff', 'corporate']:
            return render(request, 'add_user.html', {'error': 'Only staff or corporate roles allowed'})

        if User.objects.filter(username=username).exists():
            return render(request, 'add_user.html', {'error': 'Username already exists'})

        User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            role=role
        )
        return redirect('view_users')

    return render(request, 'add_user.html')

@login_required
def manage_bins(request):
    if request.user.role != 'admin':
        return render(request, '403.html')

    bins = Bin.objects.all()
    return render(request, 'manage_bins.html', {'bins': bins})

@login_required
def add_bin(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        location = request.POST.get('location')
        status = request.POST.get('status')
        fill_level = request.POST.get('fill_level')

        Bin.objects.create(
            category=category,
            location=location,
            status=status,
            fill_level=fill_level
        )
        messages.success(request, "Bin added successfully.")
        return redirect('manage_bins')

    return render(request, 'add_bin.html')


@login_required
def edit_bin(request, bin_id):
    if request.user.role != 'admin':
        return render(request, '403.html')

    bin = get_object_or_404(Bin, id=bin_id)
    locations = ['Block A', 'Block B', 'Canteen', 'Hostel', 'Library', 'Playground']

    if request.method == 'POST':
        bin.location = request.POST['location']
        bin.status = request.POST['status']
        bin.fill_level = int(request.POST['fill_level'])
        bin.save()
        return redirect('manage_bins')

    return render(request, 'edit_bin.html', {'bin': bin, 'locations': locations})


@login_required
def view_feedback(request):
    if request.user.role != 'admin':
        return render(request, '403.html')

    # Handle "Mark as Read"
    if request.method == 'POST':
        feedback_id = request.POST.get('feedback_id')
        feedback = get_object_or_404(Feedback, id=feedback_id)
        if feedback.feedback_type in ['Suggestion', 'Complaint']:
            feedback.status = 'Read'
            feedback.save()

    feedbacks = Feedback.objects.all().order_by(
        Case(
            When(feedback_type='Alert', then=0),
            default=1,
            output_field=IntegerField()
        ),
        '-created_at'
    )
    bins = Bin.objects.all()
    return render(request, 'view_feedback.html', {'feedbacks': feedbacks, 'bins': bins})


@login_required
def delete_feedback(request, feedback_id):
    if request.user.role != 'admin':
        return render(request, '403.html')

    feedback = get_object_or_404(Feedback, id=feedback_id)

    if request.method == 'POST':
        feedback.delete()
        messages.success(request, "Feedback deleted successfully.")
        return redirect('view_feedback')  # Use your feedback page name here

    return render(request, '403.html')


@login_required
def delete_bin(request, bin_id):
    if request.user.role == 'admin':
        bin = get_object_or_404(Bin, id=bin_id)
        bin.delete()
    return redirect('manage_bins')

@login_required
def edit_bin_by_location(request, id):
    if request.user.role != 'admin':
        return render(request, '403.html')

    feed = get_object_or_404(Feedback, id=id)

    try:
        bin = Bin.objects.get(location=feed.location)
    except Bin.DoesNotExist:
        return render(request, 'bin_not_found.html', {'location': feed.location})

    if request.method == 'POST':
        new_status = request.POST['status']
        new_fill = int(request.POST['fill_level'])

        bin.status = new_status
        bin.fill_level = new_fill
        bin.save()

        # ✅ Send email to corporate only if status = Full
        if new_status == "Full":
            corporate_users = User.objects.filter(role='corporate')
            for corp in corporate_users:
                if corp.email:
                    print("Sending email to:", corp.email)
                    print("Using email backend:", settings.EMAIL_BACKEND)
                    send_mail(
                        subject='🚨 Bin Marked Full - CampusEcoTrack',
                        message=f"""
Hello {corp.username},

A bin has been marked FULL by the Admin.

📍 Location: {bin.location}
🗂 Category: {bin.category or 'None'}
📊 Fill Level: {bin.fill_level}%
📅 Time: {timezone.now().strftime('%Y-%m-%d %H:%M')}

Please collect it as scheduled.

Regards,
CampusEcoTrack System
""",
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list = [corp.email, settings.EMAIL_HOST_USER],
                        fail_silently=True
                    )

        messages.success(request, "Bin updated successfully.")
        return redirect('view_feedback')

    return render(request, 'edit_bin_from_feedback.html', {'bin': bin})



@login_required
def view_collections(request):
    if request.user.role != 'admin':
        return render(request, '403.html')

    collections = BinCollection.objects.select_related('bin', 'collected_by').order_by('-collected_at')
    return render(request, 'collection_history.html', {'collections': collections})

@login_required
def mark_feedback_as_read(request, feedback_id):
    if request.user.role != 'admin':
        return render(request, '403.html')

    feedback = get_object_or_404(Feedback, id=feedback_id)

    if feedback.feedback_type in ['Suggestion', 'Complaint'] and feedback.status == 'Unread':
        feedback.status = 'Read'
        feedback.save()
        messages.success(request, "Feedback marked as read.")

    return redirect('view_feedback') 