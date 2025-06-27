from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('home',views.home, name='home'),
    path('register', views.register_view, name='register_view'),
    path('login/', views.login_view, name='login_view'),
    path('logout', views.logout_view, name='logout_view'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
]

