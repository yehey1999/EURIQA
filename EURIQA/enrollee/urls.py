from django.urls import path
from . import views

app_name = 'enrollee'

urlpatterns = [
    path('home', views.EnrolleeHomeView.as_view(), name='enrollee_home'),
    path('login', views.EnrolleeLoginView.as_view(), name='enrollee_login')
    

]