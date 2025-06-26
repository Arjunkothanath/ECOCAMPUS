from django.urls import path
from . import views

urlpatterns = [
    path('corporate_dashboard/', views.corporate_dashboard, name='corporate_dashboard'),
    path('collect/<int:bin_id>/', views.mark_bin_collected, name='mark_bin_collected'),
    path('collect_bin/<int:bin_id>/', views.collect_bin, name='collect_bin'),
    path('bins/', views.view_bins, name='corporate_view_bins'),
    path('collection_history/', views.collection_history, name='collection_history'),
    path('feedbacks', views.corporate_feedback, name='corporate_feedback'),
    path('schedule_collection/', views.schedule_collection, name='schedule_collection'),
    path('collected_bins/', views.view_collected_bins, name='corporate_view_collected_bins'),  # ✅ ADD THIS
]

