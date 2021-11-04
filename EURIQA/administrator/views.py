from django.http import Http404, HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import auth, User
from django.contrib.auth import login, logout
from django.contrib import messages
from administrator.models import *
from enrollee.models import *
# from .forms import EnrolleeRegistrationForm
# from .forms import QuestionForm

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

class AdmminProfile(View):
    def get(self,request):
        qs_admin = Administrator.objects.filter(user_id=request.user.id)
        context = {
            'admin_details': qs_admin,
        }
        
        if not request.user.is_authenticated:
            return redirect("administrator:admin_login")
        return render(request, 'administrator/adminProfile.html', context)
        
class AdminAccountRegistrationView(View):
    def get(self,request):
        qs_program = Program.objects.order_by('program_name')
        qs_strand = Strand.objects.order_by('strand_name')
        context = {
            'programs': qs_program,
            'strands': qs_strand,
        }

        if not request.user.is_authenticated:
            return redirect("administrator:admin_login")
        return render(request, 'administrator/enrolleeRegistration/adminRegForm.html', context)

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
                set_program = request.POST.get('program')
                set_strand = request.POST.get('strand')

                if set_program is None:
                    program = None
                else:
                    program = Program.objects.get(program_id=set_program)
                
                if set_strand is None:
                    strand = None
                else:
                    strand = Strand.objects.get(strand_id=set_strand)
                
                position = request.POST.get('position')
                user_type = request.POST.get('user_type')

                #Address
                street = request.POST.get('street')
                city = request.POST.get('city')
                province = request.POST.get('province')
                zip_code = request.POST.get('zip')

                full_address = street + ", " + city + ", " + province + ", " + zip_code
                
                user = User.objects.create_user(username=username, password=password, email=email, first_name=firstname, last_name=lastname)
                
            if user_type == 'enrollee':
                user_id_latest_added=User.objects.all().last()
                register_enrollee = Enrollee(user = user_id_latest_added, middle_name=middlename, address = full_address, level = level, program = program, strand = strand)
                register_enrollee.save()

            else:
                user_id_latest_added=User.objects.all().last()
                register_admin = Administrator(user = user_id_latest_added, middle_name=middlename, address = full_address, position = position)
                register_admin.save()
        messages.success(request, "Account created")

        return redirect("administrator:admin_regform")

class AdminManageAccounts(View):
    def get(self,request):
        qs_accounts = Enrollee.objects.all()
        context = {
            'accounts': qs_accounts,
        }

        if not request.user.is_authenticated:
            return redirect("administrator:admin_login")
        return render(request, 'administrator/enrolleeRegistration/adminManageAccounts.html', context)

    def post(self, request):
        if request.method == "POST":
            # Deactivate accounts that are done taking the exam
            if 'btn_deact' in request.POST:
                user_id = request.POST.get('user_id')
                exam_status = request.POST.get('exam_status')
                
                if exam_status == "done":
                    deactivate_acc = User.objects.filter(id = user_id).update(is_active=0)
                    messages.success(request, 'Account deactivated')
                else:
                    messages.error(request, 'Cannot deactivate account.')

            # Reactivate accounts that are deactivated
            if 'btn_react' in request.POST:
                deact_uid = request.POST.get('deact-user_id')
                enrollee_id = request.POST.get('enrollee_id')

                reactivate_acc = User.objects.filter(id = deact_uid).update(is_active=1)
                update_examstat = Enrollee.objects.filter(enrollee_id = enrollee_id).update(exam_status="not done")
                messages.success(request, 'Account reactivated')

        return redirect("administrator:admin_accounts")

class AdminCreateExam(View):
    def get(self,request):
        qs_question = Question.objects.all()
        context = {
            'questions': qs_question,
        }

        if not request.user.is_authenticated:
            return redirect("administrator:admin_login")
        return render(request, 'administrator/examManagement/adminCreateExam.html', context)

    def post(self, request):
        if 'btnSaveExam' in request.POST:
            exam_title = request.POST.get("exam_title")
            exam_takers = request.POST.get("exam_takers")
            
            get_admin_id = Administrator.objects.get(user_id = request.user.id)

            create_exam = Exam(title = exam_title, takers = exam_takers, created_by = get_admin_id)
            create_exam.save()
            messages.success(request, "Exam created.")

        elif 'btnSaveQuestion' in request.POST:
            # exam = request.POST.get("exam")
            # part = request.POST.get("part")
            question_no = request.POST.get("question_no")
            question = request.POST.get("question")
            optionA = request.POST.get("optionA")
            optionB = request.POST.get("optionB")
            optionC = request.POST.get("optionC")
            optionD = request.POST.get("optionD")
            answer = request.POST.get("answer")
            points = request.POST.get("points")
            
            # create_exam = Exam()
            # create_exam.save()

            
            add_question = Question(question_no = question_no, question = question, optionA = optionA, optionB = optionB, optionC = optionC, optionD = optionD, answer = answer, points = points)
            add_question.save()

            messages.success(request, "Question saved.")

        else:
            print(form.errors)
            return HttpResponse('INVALID! Question not saved.')

        return redirect("administrator:question_form")

class AdminMainExamTableView(View):
    def get(self, request):
        print("ok")
        return render(request, 'administrator/examManagement/adminManageMainExam.html')

    # def post

        