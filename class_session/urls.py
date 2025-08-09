from django.urls import path
from . import views

urlpatterns = [
    path("classroom/<str:classroom>/", views.AllSessionsView.as_view()),
    path("<int:pk>/", views.OneSessionView.as_view()),
    path("classroom/<str:classroom>/create/", views.CreateSessionView.as_view()),
    path("<int:pk>/files/", views.OneSessionFilesView.as_view()),
    path("<int:pk>/lecture/", views.UpdateLectureView.as_view()),
    path("<int:pk>/publish/", views.publish.as_view()),
]
