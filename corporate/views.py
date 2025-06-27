from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from general.models import Bin, BinCollection, Feedback
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from datetime import timedelta, date
from django.utils import timezone
from django.db.models import Q


@login_required
def corporate_dashboard(request):
    if request.user.role != 'corporate':
        return render(request, '403.html')

    total_feedbacks = Feedback.objects.filter(
        user__role__in=['student', 'staff', 'headstaff']
    ).count()

    collection_count = BinCollection.objects.count()
    collected_bins_count = BinCollection.objects.values('bin').distinct().count()

    context = {
        'total_feedbacks': total_feedbacks,
        'collection_count': collection_count,
        'collected_bins_count': collected_bins_count,
    }

    return render(request, 'corporate/dashboard.html', context)

@login_required
def mark_bin_collected(request, bin_id):
    if request.user.role != 'corporate':
        return render(request, '403.html')

    bin = get_object_or_404(Bin, id=bin_id)

    # Update bin status
    bin.status = 'Empty'
    bin.fill_level = 0
    bin.save()

    # Log collection
    BinCollection.objects.create(
        bin=bin,
        collected_by=request.user
    )

    return redirect('corporate_dashboard')

@login_required
def view_bins(request):
    if request.user.role != 'corporate':
        return render(request, '403.html')

    bins = Bin.objects.all()
    today = date.today()

    return render(request, 'corporate/view_bins.html', {
        'bins': bins,
        'today': today
    })

from datetime import date
from dateutil.relativedelta import relativedelta

@login_required
def collect_bin(request, bin_id):
    if request.user.role != 'corporate':
        return render(request, '403.html')

    bin_obj = get_object_or_404(Bin, id=bin_id)
    today = timezone.now().date()

    # ✅ Allow collection if it's Full OR it's the scheduled date
    if bin_obj.status == 'Full' or bin_obj.scheduled_date == today:
        # Reset bin
        bin_obj.status = 'Empty'
        bin_obj.fill_level = 0

        # ✅ Update next collection ONLY if collected on the scheduled day
        if bin_obj.scheduled_date == today:
            bin_obj.scheduled_date = today + relativedelta(months=1)

        bin_obj.save()

        # Mark related alert feedbacks as Resolved
        Feedback.objects.filter(
            location=bin_obj.location,
            feedback_type="Alert",
            status="Pending"
        ).update(status="Resolved")

        # Save collection record
        BinCollection.objects.create(bin=bin_obj, collected_by=request.user)

        messages.success(request, "Bin collected successfully.")

    else:
        messages.warning(request, "Cannot collect: Bin must be Full or it must be the scheduled collection day.")

    return redirect('corporate_view_bins')


@login_required
def collection_history(request):
    if request.user.role != 'corporate':
        return render(request, '403.html')

    collections = BinCollection.objects.select_related('bin', 'collected_by').order_by('-collected_at')

    return render(request, 'corporate/collection_history.html', {
        'collections': collections
    })

@login_required
def corporate_feedback(request):
    if request.user.role != 'corporate':
        return render(request, '403.html')

    feedbacks = Feedback.objects.select_related('user').order_by('-created_at')
    
    student_feedbacks = feedbacks.filter(user__role='student')
    staff_feedbacks = feedbacks.filter(user__role='staff')
    headstaff_feedbacks = feedbacks.filter(user__role='headstaff')

    return render(request, 'corporate/feedbacks.html', {
        'student_feedbacks': student_feedbacks,
        'staff_feedbacks': staff_feedbacks,
        'headstaff_feedbacks': headstaff_feedbacks
    })

@login_required
def schedule_collection(request):
    if request.user.role != 'corporate':
        return render(request, '403.html')

    all_bins = Bin.objects.all()
    selected_bin = None

    # ✅ GET: pre-select a bin if bin_id provided
    bin_id = request.GET.get('bin_id')
    if bin_id:
        try:
            selected_bin = Bin.objects.get(id=bin_id)
        except Bin.DoesNotExist:
            selected_bin = None
            messages.error(request, "The selected bin does not exist.")

    # ✅ POST: update scheduled date
    if request.method == 'POST':
        bin_id = request.POST.get('bin')
        schedule_date = request.POST.get('schedule_date')

        if not bin_id or not schedule_date:
            messages.error(request, "Please select a bin and date.")
            return redirect('schedule_collection')

        try:
            bin_obj = Bin.objects.get(id=bin_id)
            bin_obj.scheduled_date = schedule_date
            bin_obj.save()
            print("Schedule Date Submitted:", schedule_date)
            messages.success(request, "Collection date scheduled successfully.")
            return redirect('corporate_view_bins')
        except Bin.DoesNotExist:
            messages.error(request, "Invalid bin selected.")
            return redirect('schedule_collection')

    return render(request, 'corporate/schedule_collection.html', {
        'bins': all_bins,
        'selected_bin': selected_bin
    })

@login_required
def view_collected_bins(request):
    if request.user.role != 'corporate':
        return render(request, '403.html')

    collections = BinCollection.objects.select_related('bin', 'collected_by').order_by('-collected_at')

    return render(request, 'corporate/view_collected_bins.html', {
        'collections': collections,
        'collected_bins_count': collections.count()
    })
# Create your views here.
