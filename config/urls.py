from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin-panel/', admin.site.urls),
    path('', include('accounts.urls')),
    path('lessons/', include('lessons.urls')),
    path('attendance/', include('attendance.urls')),
]
