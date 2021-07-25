from django.http import Http404, HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import auth, User
from django.contrib.auth import login, logout
from django.contrib import messages
from enrollee.models import *
# Create your views here.

class EnrolleeLoginView(View):
    def get(self, request):
        return render(request, 'enrolleeLogin.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        

        if user is not None:
            auth.login(request, user)
            is_enrollee = Enrollee.objects.filter(user_id=request.user.id)

            if is_enrollee:
                return redirect('enrollee:dummy')  # Change to redirect to confirmation page

            else:
                messages.error(request,"Your account is unauthorized to log in.")
                return redirect("enrollee:enrollee_login")   

        else:
            messages.error(request, 'Invalid username or password.')
            return redirect("enrollee:enrollee_login")

class DummyView(View):
    def get(self, request):
        return render(request, 'dummy.html')