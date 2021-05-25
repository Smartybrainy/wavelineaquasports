from django.urls import path
from .views import HomeView, AboutUs, Programs

app_name = "sport"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutUs.as_view(), name='about'),
    path('programs/', Programs.as_view(), name='programs'),
]
