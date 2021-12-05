from django.http import Http404, HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import auth, User
from django.contrib.auth import login, logout
from django.contrib import messages
from enrollee.models import *
from administrator.models import *

# Create your views here.

class EnrolleeHomeView(View):
    def get(self, request):
        return render(request, 'enrollee/enrolleeHome.html')

class EnrolleeLoginView(View):
    def get(self, request):
        return render(request, 'enrollee/enrolleeLogin.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            is_enrollee = Enrollee.objects.filter(user_id=request.user.id)

            if is_enrollee:
                return redirect('enrollee:enrollee_details')

            else:
                messages.error(request,"Your account is unauthorized to log in.")
                return redirect("enrollee:enrollee_login")   

        else:
            messages.error(request, 'Invalid username or password.')
            return redirect("enrollee:enrollee_login")

class EnrolleeLogoutView(View):
    def get(self,request):
        logout(request)
        return  redirect("enrollee:enrollee_login")

    def post(self,request):
        logout(request)
        return  redirect("enrollee:enrollee_login")

class EnrolleeDetailsCheckView(View):
    def get(self, request):
        qs_enrollee = Enrollee.objects.filter(user_id=request.user.id)

        print(qs_enrollee)

        context = {
            'enrollees' : qs_enrollee,
        }

        if not request.user.is_authenticated:
            return redirect("enrollee:enrollee_login")
        return render(request, 'enrollee/enrolleeDetails.html', context)

class EnrolleeTermsView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("enrollee:enrollee_login")
        return render(request, 'enrollee/enrolleeTerms.html')

class EnrolleeDataPolicyView(View):
    def get(self, request):
        qs_exam = Exam.objects.all()
        if not request.user.is_authenticated:
            return redirect("enrollee:enrollee_login")
        return render(request, 'enrollee/enrolleeDataPolicy.html')

class EnrolleeCaptureImageView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("enrollee:enrollee_login")
        return render(request, 'enrollee/enrolleeCaptureImage.html')

class EnrolleeInstructionsView(View):
    def get(self, request):
        qs_enrollee = Enrollee.objects.filter(user = request.user.id)
        
        get_level = Enrollee.objects.filter(user = request.user.id).values_list('level', flat=True)
        check_level = Enrollee.objects.filter(user = request.user.id).get(level__in = get_level)
        
        if check_level.level == "college":
            qs_exam = Exam.objects.filter(takers="College")

        elif check_level.level == "shs":
            qs_exam = Exam.objects.filter(takers="Senior High School")
        
        elif check_level.level == "jhs":
            qs_exam = Exam.objects.filter(takers="Junior High School")
        
        elif check_level.level == "elem":
            qs_exam = Exam.objects.filter(takers="Elementary")
        
        else:
            print("level does not exist")

        get_exam_id = qs_exam.values_list('exam_id', flat=True)

        qs_part = Part.objects.filter(exam__in = get_exam_id)

        context = {
            'exams': qs_exam,
            'enrollee': qs_enrollee,
            'parts': qs_part,
        }

        if not request.user.is_authenticated:
            return redirect("enrollee:enrollee_login")
        return render(request, 'enrollee/enrolleeInstructions.html', context)
    
class EnrolleeExamCompletionView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("enrollee:enrollee_login")
        return render(request, 'enrollee/enrolleeExamCompletion.html')

def exam_page(request, exam_id=None, part_id=None):
    get_level = Enrollee.objects.filter(user = request.user.id).values_list('level', flat=True)
    check_level = Enrollee.objects.filter(user = request.user.id).get(level__in = get_level)
    
    if check_level.level == "college":
        qs_exam = Exam.objects.filter(takers="College")

    elif check_level.level == "shs":
        qs_exam = Exam.objects.filter(takers="Senior High School")
    
    elif check_level.level == "jhs":
        qs_exam = Exam.objects.filter(takers="Junior High School")
    
    elif check_level.level == "elem":
        qs_exam = Exam.objects.filter(takers="Elementary")
    
    else:
        print("level does not exist")

    get_exam_id = qs_exam.values_list('exam_id', flat=True)

    qs_part = Part.objects.filter(part_id = part_id)
    qs_question = Question.objects.filter(exam_id = exam_id).filter(part = part_id)
    
    context = {
        'exams': qs_exam,
        'parts': qs_part,
        'questions': qs_question,
    }

    if not request.user.is_authenticated:
        return redirect("enrollee:enrollee_login")
    return render(request, 'enrollee/enrolleeExam.html', context)