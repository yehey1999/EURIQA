from django.urls import path
from . import views

app_name = 'administrator'

urlpatterns = [
    path('login', views.AdminLoginView.as_view(), name='admin_login'),
    path('logout', views.AdminLogoutView.as_view(), name='admin_logout'),
    path('home', views.AdminHomeView.as_view(), name='admin_home'),
    path('dashboard', views.AdminDashboard.as_view(), name='admin_dashboard'),
    path('profile', views.AdmminProfile.as_view(), name='admin_profile'),
    path('enrollee-management/regform', views.AdminAccountRegistrationView.as_view(), name='admin_regform'),
    path('enrollee-management/accounts', views.AdminManageAccounts.as_view(), name='admin_accounts'),
    path('exam-management/questionform', views.AdminQuestionCreateView.as_view(), name='question_form'),
    path('exam-management/mainexamtable', views.AdminMainExamTableView.as_view(), name='mainexam_table'),
]