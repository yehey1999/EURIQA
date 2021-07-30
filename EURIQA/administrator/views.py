from django.http import Http404, HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import auth, User
from django.contrib.auth import login, logout
from django.contrib import messages
from administrator.models import *

# Create your views here.

class AdminLoginView(View):
    def get(self, request):
        return render(request, 'adminLogin.html')

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
        return render(request, 'adminHome.html')

class AdminAccountRegistrationView(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect("administrator:admin_login")
        return render(request, 'adminRegForm.html')