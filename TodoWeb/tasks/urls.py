from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tasks/', views.task_list, name='task_list'),
    path('register/', views.register, name='register'),
    path('create/', views.create_task, name='create_task'),
    path('update/<str:task_id>/', views.update_task, name='update_task'),
    path('delete/<str:task_id>/', views.delete_task, name='delete_task'),
    path('toggle/<str:task_id>/', views.toggle_task, name='toggle_task'),
    path('google-login/', views.google_login, name='google_login'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
    path('account/', views.account, name='account'),
] 