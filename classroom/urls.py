from django.urls import path
from . import views

urlpatterns = [
  
  path('', views.HomeClassRoom.as_view()),
  path('<str:id>/', views.ClassRoomView.as_view()),
  path('<str:id>/join/', views.JoinClassRoom.as_view()),
  path('<str:id>/leave/', views.LeaveClassRoom.as_view()),
  path('<str:id>/admin/<int:pk>/', views.AdminClassRoom.as_view()),
  path('<str:id>/approve/', views.MemberApproveView.as_view()),
  path('<str:id>/approve/', views.AdminRemoveView.as_view()),
  
]