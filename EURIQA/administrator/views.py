from django.http import Http404, HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import auth, User
from django.contrib.auth import login, logout
from django.contrib import messages
from administrator.models import *
from enrollee.models import *
# from .forms import RegistrationForm

# Create your views here.

class AdminLoginView(View):
    def get(self, request):
        return render(request, 'administrator/adminLogin.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            is_admin = Administrator.objects.filter(user_id=request.user.id)

            if is_admin:
                return redirect('administrator:admin_home')

            else:
                messages.error(request,"Your account is unauthorized to log in.")
                return redirect("administrator:admin_login")   

        else:
            messages.error(request, 'Invalid username or password.')
            return redirect("administrator:admin_login")

class AdminLogoutView(View):
    def get(self,request):
        logout(request)
        return  redirect("administrator:admin_login")

    def post(self,request):
        logout(request)
        return  redirect("administrator:admin_login")

class AdminHomeView(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect("administrator:admin_login")
        return render(request, 'administrator/adminHome.html')

class AdminDashboard(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect("administrator:admin_login")
        return render(request, 'administrator/adminDashboard.html')

class AdminAccountRegistrationView(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect("administrator:admin_login")
        return render(request, 'administrator/adminRegForm.html')

    def post(self, request):
        if request.method == 'POST':
            if 'btnSubmit' in request.POST:
                username = request.POST.get('username')
                password = request.POST.get('password')
                email = request.POST.get('email')
                firstname = request.POST.get('first_name')
                middlename = request.POST.get('middle_name')
                lastname = request.POST.get('last_name')
                level = request.POST.get('level')

                #Address
                street = request.POST.get('street')
                city = request.POST.get('city')
                province = request.POST.get('province')
                zip_code = request.POST.get('zip')

                full_address = street + ", " + city + ", " + province + ", " + zip_code
                
                user = User.objects.create_user(username=username, password=password, email=email, first_name=firstname, last_name=lastname)

        messages.success(request, "Account created")
        return render(request, 'administrator/adminRegForm.html')

class AdminManageAccounts(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect("administrator:admin_login")
        return render(request, 'administrator/adminManageAccounts.html')
