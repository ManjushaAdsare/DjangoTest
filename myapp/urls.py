from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # path('', include('myproject.urls')),
    path('', views.List_Candidates.as_view()),
    path('save-candidate/', views.AddCandidateData.as_view()),
    path('save-pdf/',views.CreateResume.as_view())
]
