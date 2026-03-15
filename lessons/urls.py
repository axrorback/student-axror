from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("lessons/", views.lessons_list_view, name="lessons_list"),
    path("lessons/<uuid:pk>/", views.lesson_detail_view, name="lesson_detail"),
    path("assignments/<uuid:assignment_id>/submit/", views.assignment_submit_view, name="assignment_submit"),
    path("submissions/<uuid:submission_id>/review/", views.submission_review_detail_view, name="submission_review_detail"),
    path("leaders/", views.leaderboard_view, name="leaderboard"),
]