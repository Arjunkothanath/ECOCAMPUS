from django.urls import path
from . import views

urlpatterns = [
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/submit-feedback/', views.submit_feedback, name='submit_feedback'),
    path('staff/view-feedbacks/', views.combined_feedback_view, name='view_feedbacks'),
    path('staff/students/', views.view_students, name='view_students'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('submit_feedback/', views.submit_feedback_student, name='submit_feedback_student'),
    path('my_feedbacks/', views.view_feedback_student, name='view_feedback_student'),
    
]
