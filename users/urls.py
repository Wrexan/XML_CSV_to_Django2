from django.urls import path

from . import views

urlpatterns = [
    path('', views.UserList.as_view()),
    path('upload/', views.UserUploadFormView.as_view()),
    ]
