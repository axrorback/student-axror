from django.urls import path
from .views import student_login_view , student_logout_view , profile_view
urlpatterns = [
    path('login/', student_login_view, name='student_login'),
    path('logout/', student_logout_view, name='student_logout'),
    path('profile/', profile_view, name='profile'),
]