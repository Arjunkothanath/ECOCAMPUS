from django.urls import path
from . import views

urlpatterns = [
    path('headstaff_dashboard', views.headstaff_dashboard, name='headstaff_dashboard'),
    path('add-staff/', views.add_staff_by_head, name='add_staff_by_head'),
    path('feedbacks/', views.view_feedback_by_headstaff, name='view_head_feedback'),
    path('users/', views.view_users_by_headstaff, name='headstaff_view_users'),
    path('manage-staff/', views.manage_staff, name='manage_staff'),
    path('edit-staff/<int:user_id>/', views.edit_staff, name='edit_staff'),
    path('delete-staff/<int:user_id>/', views.delete_staff, name='delete_staff'),
    path('submit_feedback', views.submit_feedback_headstaff, name='submit_feedback_headstaff'),

]
