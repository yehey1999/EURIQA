from django.urls import path
from . import views

app_name = 'enrollee'

urlpatterns = [
    path('home', views.EnrolleeHomeView.as_view(), name='enrollee_home'),
    path('login', views.EnrolleeLoginView.as_view(), name='enrollee_login'),
    path('logout', views.EnrolleeLogoutView.as_view(), name='enrollee_logout'),
    path('details', views.EnrolleeDetailsCheckView.as_view(), name='enrollee_details'),
    path('terms', views.EnrolleeTermsView.as_view(), name='enrollee_terms'),
    path('datapolicy', views.EnrolleeDataPolicyView.as_view(), name='enrollee_datapolicy'),
    path('captureimage', views.EnrolleeCaptureImageView.as_view(), name='enrollee_captureimage'),
    path('instructions', views.EnrolleeInstructionsView.as_view(), name='enrollee_instructions'),
    path('exam/<int:exam_id>/<int:part_id>', views.exam_page, name='enrollee_exam'),
    path('results/<int:enrollee_id>/<int:exam_id>', views.exam_results, name='enrollee_examcompletion'),
]