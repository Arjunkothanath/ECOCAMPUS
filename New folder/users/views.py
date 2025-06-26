from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from general.models import Feedback, User, Bin
from django.utils import timezone
from django.contrib import messages


@login_required
def staff_dashboard(request):
    if request.user.role != 'staff':
        return render(request, '403.html')

    student_count = User.objects.filter(role='student').count()
    student_feedback_count = Feedback.objects.filter(user__role='student').count()
    my_feedback_count = Feedback.objects.filter(user=request.user).count()

    return render(request, 'staff/dashboard.html', {
        'student_count': student_count,
        'student_feedback_count': student_feedback_count,
        'my_feedback_count': my_feedback_count
    })

@login_required
def submit_feedback(request):
    if request.user.role != 'staff':
        return render(request, '403.html')

    if request.method == 'POST':
        feedback_type = request.POST.get('type')
        category = request.POST.get('category')
        location = request.POST.get('location')
        other_location = request.POST.get('other_location')
        message = request.POST.get('message')

        final_location = other_location if location == 'Others' else location

        if feedback_type == 'Alert' and not final_location:
            messages.error(request, "Please specify a valid bin location for alerts.")
            return redirect('submit_feedback')

        Feedback.objects.create(
            user=request.user,
            feedback_type=feedback_type,
            location=final_location,
            message=message,
            status="Pending" if feedback_type == "Alert" else "Unread",
            created_at=timezone.now()
        )
        messages.success(request, "Feedback submitted successfully.")
        return redirect('view_feedbacks')

    bins = Bin.objects.all()
    categories = sorted(set(bin.category for bin in bins))

    return render(request, 'staff/submit_feedback.html', {
        'bins': bins,
        'categories': categories
    })

@login_required
def combined_feedback_view(request):
    if request.user.role != 'staff':
        return render(request, '403.html')

    my_feedbacks = Feedback.objects.filter(user=request.user).order_by('-created_at')
    student_feedbacks = Feedback.objects.filter(user__role='student').order_by('-created_at')

    bins = Bin.objects.all()
    return render(request, 'staff/view_feedback.html', {
        'my_feedbacks': my_feedbacks,
        'student_feedbacks': student_feedbacks,
        'bins': bins,
    })



@login_required
def view_students(request):
    if request.user.role != 'staff':
        return render(request, '403.html')

    students = User.objects.filter(role='student').order_by('username')

    return render(request, 'staff/view_students.html', {
        'students': students
    })



@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return render(request, '403.html')
    return render(request, 'student/student_dashboard.html')

@login_required
def submit_feedback_student(request):
    if request.user.role != 'student':
        return render(request, '403.html')

    bins = Bin.objects.all()

    if request.method == 'POST':
        feedback_type = request.POST.get('type')
        message = request.POST.get('message')
        location = request.POST.get('location')
        other_location = request.POST.get('other_location')

        final_location = other_location if location == 'Others' else location

        if feedback_type == "Alert" and not final_location:
            messages.error(request, "Please select or enter a valid location for alert.")
            return redirect('submit_feedback_student')

        Feedback.objects.create(
            user=request.user,
            feedback_type=feedback_type,
            location=final_location or "",
            message=message,
            status="Pending" if feedback_type == "Alert" else "Unread",
            created_at=timezone.now()
        )

        messages.success(request, "Feedback submitted successfully.")
        return redirect('student_dashboard')

    return render(request, 'student/submit_feedback_student.html', {
        'bins': bins
    })


@login_required
def view_feedback_student(request):
    if request.user.role != 'student':
        return render(request, '403.html')

    feedbacks = Feedback.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'student/view_feedback_student.html', {'feedbacks': feedbacks})

