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
    path('exam-management/create-exam', views.AdminCreateExam.as_view(), name='admin_create_exam'),
    path('exam-management/exam-details', views.AdminAddQuestion.as_view(), name='admin_exam_details'),
    path('exam-management/all-exams', views.AdminViewAllExamsTable.as_view(), name='all-exams'),
    path('exam-management/edit-exam/<int:exam_id>/', views.view_exam, name='edit-exams'),
]   