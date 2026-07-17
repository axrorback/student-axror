from django.urls import path

from .views import *

urlpatterns = [
    path('courses/',courses,name='courses'),
    path('pay/<uuid:uuid>/',pay_course,name='pay_course'),
    path('click/callback/',payment_callback,name='payment_callback'),
    path('payment/status/<uuid:uuid>/',payment_success,name='payment_success'),
]