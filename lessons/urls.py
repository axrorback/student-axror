# lessons/urls.py
from django.urls import path
from .views import dashboard_view, lessons_list_view, lesson_detail_view

urlpatterns = [
    path("", dashboard_view, name="dashboard"),
    path("lessons/", lessons_list_view, name="lessons_list"),
    path("lessons/<uuid:pk>/", lesson_detail_view, name="lesson_detail"),
]
