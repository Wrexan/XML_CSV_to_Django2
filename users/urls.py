from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.UserList.as_view()),
    path('upload/', views.UserUploadFormView.as_view()),
    path('', include('django.contrib.auth.urls')),
    ]
