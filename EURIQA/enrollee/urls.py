from django.urls import path
from . import views

app_name = 'enrollee'

urlpatterns = [
    path('login', views.EnrolleeLoginView.as_view(), name='enrollee_login'),
    path('dummy', views.DummyView.as_view(), name='dummy')

]