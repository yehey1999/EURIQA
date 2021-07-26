from django.urls import path
from . import views

app_name = 'enrollee'

urlpatterns = [
    path('home', views.EnrolleeHomeView.as_view(), name='enrollee_home'),
    path('login', views.EnrolleeLoginView.as_view(), name='enrollee_login'),
    path('logout', views.EnrolleeLogoutView.as_view(), name='enrollee_logout'),
    path('details', views.EnrolleeDetailsCheckView.as_view(), name='enrollee_details'),
    path('terms', views.EnrolleeTermsView.as_view(), name='enrollee_terms')
]