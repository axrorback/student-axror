from django.urls import path
from codepaste.views import create_paste , share_paste

urlpatterns = [
    path('create/', create_paste, name='create_paste'),
    path("share/<str:username>/<str:language>/<int:id>/",share_paste,name="share_paste"),
]