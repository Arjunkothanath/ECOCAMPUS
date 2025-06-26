from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect


class User(AbstractUser):
    
    role = models.CharField(max_length=10, default='admin')

    def __str__(self):
        return f"{self.username} ({self.role})"

class Bin(models.Model):
    CATEGORY_CHOICES = [
        ('Dry', 'Dry'),
        ('Wet', 'Wet'),
        ('Plastic', 'Plastic'),
        ('E-Waste', 'E-Waste'),
        ('Other', 'Other'),
    ]
    LOCATION_CHOICES = [
        ('Block A', 'Block A'),
        ('Block B', 'Block B'),
        ('Canteen', 'Canteen'),
        ('Hostel', 'Hostel'),
        ('Library', 'Library'),
        ('Playground', 'Playground'),
    ]
    
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=[('Empty', 'Empty'), ('Full', 'Full')], default='Empty')
    fill_level = models.IntegerField(default=0)  # % full (0 to 100)
    last_updated = models.DateTimeField(auto_now=True)
    scheduled_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.location} - {self.status} ({self.fill_level}%)"

class Feedback(models.Model):
    FEEDBACK_TYPE_CHOICES = (
        ('Alert', 'Alert'),
        ('Suggestion', 'Suggestion'),
        ('Complaint', 'Complaint'),
    )

    STATUS_ALERT = (
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved'),
    )

    STATUS_OTHER = (
        ('Unread', 'Unread'),
        ('Read', 'Read'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPE_CHOICES)
    location = models.CharField(max_length=100)
    message = models.TextField()
    status = models.CharField(max_length=20, default='Unread')  # Default for suggestion/complaint
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.feedback_type} - {self.location}"


class BinCollection(models.Model):
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE)
    collected_by = models.ForeignKey(User, on_delete=models.CASCADE)
    collected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bin.location} collected by {self.collected_by.username} on {self.collected_at}"
    
@login_required
def collect_bin(request, bin_id):
    if request.user.role != 'corporate':
        return render(request, '403.html')

    bin = get_object_or_404(Bin, id=bin_id)

    BinCollection.objects.create(
        bin=bin,
        collected_by=request.user
    )

    # Optional: update bin status to "Empty" after collection
    bin.status = "Empty"
    bin.fill_level = 0
    bin.save()

    return redirect('view_corporate_bins')