from django.urls import path
from . import views

urlpatterns = [
    path("classroom/<str:classroom>/", views.AllSessionsView.as_view()),
    path("<int:pk>/", views.OneSessionView.as_view()),
    path("classroom/<str:classroom>/create/", views.CreateSessionView.as_view()),
    path("<int:pk>/files/", views.OneSessionFilesView.as_view()),
    path("<int:pk>/lecture/", views.UpdateLectureView.as_view()),
    path("<int:pk>/publish/", views.publish.as_view()),
    path('<int:pk>/upload-image/<str:obj>/<int:i>/', views.UploadImage.as_view()),
    path('<int:pk>/upload-file/<str:obj>/<int:i>/', views.UploadFile.as_view()),
    path('<int:pk>/fetch-file/<str:obj>/<int:i>/', views.FetchFile.as_view()),
    path('<int:pk>/fetch-images/<str:obj>/<int:i>/', views.FetchImages.as_view()),
]
