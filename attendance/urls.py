from django.urls import path
from . import views

urlpatterns = [
    path('session/<int:pk>/', views.AllAttendance.as_view()),
    path('session/<int:pk>/attend/', views.AttendSession.as_view()),
]