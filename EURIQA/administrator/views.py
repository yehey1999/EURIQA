from django.http import Http404, HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import auth, User
from django.contrib.auth import login, logout
from django.contrib import messages
from administrator.models import *
from enrollee.models import *
from django.db import connection
from django.db.models import Sum
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
        qs_admin = Administrator.objects.filter(user_id=request.user.id)
        context = {
            'admin_details': qs_admin,
        }

        if not request.user.is_authenticated:
            return redirect("administrator:admin_login")
        return render(request, 'administrator/adminHome.html', context)

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
                enrolled_as = request.POST.get('enrolled_as')

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
                register_enrollee = Enrollee(user = user_id_latest_added, middle_name=middlename, address = full_address, level = level, program = program, strand = strand, enrolled_as = enrolled_as)
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
        if not request.user.is_authenticated:
            return redirect("administrator:admin_login")
        return render(request, 'administrator/examManagement/adminCreateExam.html')

    def post(self, request):
        if 'btnSaveExam' in request.POST:
            exam_title = request.POST.get("exam_title")
            exam_takers = request.POST.get("exam_takers")
            link = request.POST.get("link")
            
            get_admin_id = Administrator.objects.get(user_id = request.user.id)
            
            create_exam = Exam(title = exam_title, takers = exam_takers, created_by = get_admin_id, link = link)
            create_exam.save()
            messages.success(request, "Exam created.")

        else:
            messages.error(request, "Failed to create exam.")

        if link is None:
            return redirect("administrator:admin_exam_details")
        else:
            return redirect("administrator:admin_create_exam")

class AdminAddQuestion(View):
    def get(self,request):
        latest_exam = Exam.objects.last()

        qs_exam = Exam.objects.all()
        qs_parts = Part.objects.filter(exam_id = latest_exam)
        qs_questions = Question.objects.filter(exam = latest_exam)

        context = {
            'latest_exam': qs_exam,
            'parts': qs_parts,
            'questions': qs_questions,
        }

        if not request.user.is_authenticated:
            return redirect("administrator:admin_login")
        
        if latest_exam:
            latest_exam_id = latest_exam.pk
            get_exam = Exam.objects.filter(exam_id = latest_exam_id)

            print(get_exam.filter(link__isnull=True))

            if get_exam.filter(link__isnull=True): 
                return render(request, 'administrator/examManagement/adminAddQuestion.html', context)
            else:
                 messages.error(request, "Can't add questions to a linked exam.")
                 return redirect("administrator:admin_create_exam")
        
        else:
            messages.error(request, "No exam found in database")
            return redirect("administrator:admin_create_exam")

    def post(self, request):
        # Method to create exam parts
        if 'btnSavePart' in request.POST:
            part_name = request.POST.get("part_name")
            instruction = request.POST.get("instruction")
            exam_id = request.POST.get("exam_id")

            get_exam_id = Exam.objects.get(exam_id = exam_id)
            print(get_exam_id)
            
            add_part = Part(part_name = part_name, instructions = instruction, exam = get_exam_id)
            add_part.save()

            messages.success(request, "Part saved.")

        # Method to create exam questions
        elif 'btnSaveQuestion' in request.POST:
            exam_id = request.POST.get("exam_id")
            part = request.POST.get("part")
            question_no = request.POST.get("question_no")
            question = request.POST.get("question")
            optionA = request.POST.get("optionA")
            optionB = request.POST.get("optionB")
            optionC = request.POST.get("optionC")
            optionD = request.POST.get("optionD")
            points = request.POST.get("points")
            answer = request.POST.get("option")


            get_exam_id = Exam.objects.get(exam_id = exam_id)
            get_part_id = Part.objects.get(part_id = part)

            add_question = Question(question_no = question_no, exam = get_exam_id, part = get_part_id, question = question, optionA = optionA, optionB = optionB, 
                optionC = optionC, optionD = optionD, answer = answer, points = points)
            add_question.save()

            # Update total exam items and overall points of Exam
            total_items = Question.objects.filter(exam = get_exam_id).count()
            total_points = Question.objects.filter(exam = get_exam_id).aggregate(Sum('points')).get('points__sum')
            
            update_total_items = Exam.objects.filter(exam_id = exam_id).update(total_items = total_items)
            update_total_points = Exam.objects.filter(exam_id = exam_id).update(overall_points = total_points)

            # Update overall points of the particular Exam Part
            part_overall_pts = Question.objects.filter(part = get_part_id).aggregate(Sum('points')).get('points__sum')

            update_part_overall_pts = Part.objects.filter(part_id = part).update(overall_points = part_overall_pts)
            messages.success(request, "Question saved.")
        
        # Method to delete question
        elif 'btnDelQues' in request.POST:
            exam_to_delete = request.POST.get("exam_to_delete")
            part = request.POST.get("part")

            get_exam_id = Exam.objects.get(exam_id = exam_to_delete)
            get_part_id = Part.objects.get(part_id = part)
            del_ques = Question.objects.filter(question_id = exam_to_delete).delete()
            
            # Update total exam items and overall points of Exam after deleting
            total_items = Question.objects.filter(exam = get_exam_id).count()
            total_points = Question.objects.filter(exam = get_exam_id).aggregate(Sum('points')).get('points__sum')

            update_total_items = Exam.objects.filter(exam_id = exam_to_delete).update(total_items = total_items)
            update_total_points = Exam.objects.filter(exam_id = exam_to_delete).update(overall_points = total_points)
            
            # Update overall points of the particular Exam Part
            part_overall_pts = Question.objects.filter(part = get_part_id).aggregate(Sum('points')).get('points__sum')

            update_part_overall_pts = Part.objects.filter(part_id = part).update(overall_points = part_overall_pts)
            messages.success(request, "Question saved.")

            messages.success(request, "Successfully deleted question.")

        # Not working yet (Method to update question)  
        elif 'btnSaveEdited' in request.POST:
            ques_id = request.POST.get("ques_id")
            part = request.POST.get("edit_part")
            question_no = request.POST.get("edit_question_no")
            question = request.POST.get("edit_question")
            optionA = request.POST.get("edit_optionA")
            optionB = request.POST.get("edit_optionB")
            optionC = request.POST.get("edit_optionC")
            optionD = request.POST.get("edit_optionD")
            answer = request.POST.get("edit_answer")
            points = request.POST.get("edit_points")

            get_part_id = Part.objects.get(part_id = part)

            edit_question = Question.objects.filter(question_id = ques_id).update(question_no = question_no, part = get_part_id, question = question, optionA = optionA, optionB = optionB, 
                optionC = optionC, optionD = optionD, answer = answer, points = points)
            
            part_overall_pts = Question.objects.filter(part = get_part_id).aggregate(Sum('points')).get('points__sum')

            update_part_overall_pts = Part.objects.filter(part_id = part).update(overall_points = part_overall_pts)

            messages.success(request, "Question edited successfully.")
        else:
            messages.error(request, "Failed to process query.")
  
        return redirect("administrator:admin_exam_details")

class AdminViewAllExamsTable(View):
    def get(self, request):
        qs_exam = Exam.objects.all()

        context = {
            'exams': qs_exam,
        }

        if not request.user.is_authenticated:
            return redirect("administrator:admin_login")
        return render(request, 'administrator/examManagement/adminAllExams.html', context)

    def post(self, request):
        if request.method == "POST":
            if 'btnDelExam' in request.POST:
                exam_to_delete = request.POST.get("exam_to_delete")

                del_ques = Exam.objects.filter(exam_id = exam_to_delete).delete()
                messages.success(request, "Successfully deleted question.")

        return redirect("administrator:all-exams")
