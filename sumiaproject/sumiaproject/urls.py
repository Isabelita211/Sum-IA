from django.urls import include, path

urlpatterns = [
    path('analysis/', include('analysis.urls')),
]