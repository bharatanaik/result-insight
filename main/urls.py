from django.urls import path
from main import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about', views.AboutView.as_view(), name='about'),
    path('upload', views.UploadView.as_view(), name='upload')
]