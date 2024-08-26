from django.urls import path
from . import views

urlpatterns = [
    path('analysis/upload/', views.upload_file, name='upload_file'),
]