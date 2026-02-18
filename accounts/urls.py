from django.urls import path
from .views import student_login_view , student_logout_view , profile_view , feedback_create_view
urlpatterns = [
    path('', student_login_view, name='student_login'),
    path('logout/', student_logout_view, name='student_logout'),
    path('profile/', profile_view, name='profile'),
    path('feedback/', feedback_create_view, name='feedback'),
]