# campusecotrack/admins/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('view_users', views.view_users, name='view_users'),
    path('add_user', views.add_user, name='add_user'),
    path('manage_bins', views.manage_bins, name='manage_bins'),
    path('manage_bins/add/', views.add_bin, name='add_bin'),
    path('manage_bins/edit/<int:bin_id>/', views.edit_bin, name='edit_bin'),
    path('manage_bins/delete/<int:bin_id>/', views.delete_bin, name='delete_bin'),
    path('feedback/', views.view_feedback, name='view_feedback'),
    path('bins/edit-by-location/<int:id>/', views.edit_bin_by_location, name='edit_bin_by_location'),
    path('collection-history/', views.view_collections, name='view_collections'),
    path('delete-feedback/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),
    path('mark-read/<int:feedback_id>/', views.mark_feedback_as_read, name='mark_feedback_as_read'),

]
