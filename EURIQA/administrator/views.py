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
from django.core.files.storage import FileSystemStorage
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
        qs_admin = Administrator.objects.filter(user_id=request.user.id)

        context = {
            'admin_details': qs_admin,
        }
        
        if not request.user.is_authenticated:
            return redirect("administrator:admin_login")
        return render(request, 'administrator/adminDashboard.html', context)

class AdmminProfile(View):
    def get(self,request):
        qs_admin = Administrator.objects.filter(user_id=request.user.id)
        context = {
            'admin_details': qs_admin,
        }
        
        if not request.user.is_authenticated:
            return redirect("administrator:admin_login")
        return render(request, 'administrator/adminProfile.html', context)

    # admin_details = read by the template

    def post(self, request):
        if request.method == 'POST':
            if 'saveBtn' in request.POST:   
                print('change profile button clicked')
                firstname = request.POST.get("update_first_name")
                middlename = request.POST.get("update_middle_name")
                lastname = request.POST.get("update_last_name")
                address = request.POST.get("update_address")
                position = request.POST.get("update_position")
                username = request.POST.get("update_username")

                picture = request.FILES['picture']
                fileSystemStorage = FileSystemStorage()
                filename = fileSystemStorage.save(picture.name, picture)
                picture = fileSystemStorage.url(filename)


                update_admin = Administrator.objects.filter(user_id = request.user.id).update(
                    picture = picture,
                    middle_name = middlename,
                    address = address,
                    position = position
                    )

                update_user = User.objects.filter(id = request.user.id).update(
                    first_name = firstname,
                    last_name = lastname,
                    username = username)

                print(update_admin)
                print('profile updated!')
                print('added image')

            # return HttpResponse ('post')
            return redirect("administrator:admin_profile")
        
class AdminAccountRegistrationView(View):
    def get(self,request):
        qs_program = Program.objects.order_by('program_name')
        qs_strand = Strand.objects.order_by('strand_name')
        qs_admin = Administrator.objects.filter(user_id=request.user.id)
        
        context = {
            'admin_details': qs_admin,
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
                
                # Can easily update the number of enrollees for we set either program and strand to null if they received no input from the template
                # Update total enrollees in Program
                total_enrollees_col = Enrollee.objects.filter(program = set_program).count()
                update_enrollees_col = Program.objects.filter(program_id = set_program).update(num_enrollees = total_enrollees_col)
                
                # Update total enrollees in Strand
                total_enrollees_shs = Enrollee.objects.filter(strand = set_strand).count()
                update_total_enrollees_shs = Strand.objects.filter(strand_id = set_strand).update(num_enrollees = total_enrollees_shs)

            else:
                user_id_latest_added=User.objects.all().last()
                register_admin = Administrator(user = user_id_latest_added, middle_name=middlename, address = full_address, position = position)
                register_admin.save()

        messages.success(request, "Account created")

        return redirect("administrator:admin_regform")

class AdminManageAccounts(View):
    def get(self,request):
        qs_accounts = Enrollee.objects.all()
        qs_admin = Administrator.objects.filter(user_id=request.user.id)
        
        context = {
            'admin_details': qs_admin,
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
                exam_status = request.POST.get("exam_status")
                program_id = request.POST.get("program_id")
                
                if exam_status == "done":
                    deactivate_acc = User.objects.filter(id = user_id).update(is_active=0)

                    # Update total enrollees in Program
                    check_isactive = User.objects.filter(is_active = 1).values_list('id', flat=True)
                    get_enrollee = Enrollee.objects.filter(enrollee_id__in = check_isactive).values_list('program', flat=True)
                    
                    # Update total enrollees in Program
                    total_enrollees_col = Enrollee.objects.filter(program__in = get_enrollee).count()
                    update_enrollees_col = Program.objects.filter(program_id = program_id).update(num_enrollees = total_enrollees_col)
                    

                    messages.success(request, 'Account deactivated')
                else:
                    messages.error(request, 'Cannot deactivate account. Enrollee has not taken the exam yet.')

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
        qs_admin = Administrator.objects.filter(user_id=request.user.id)

        context = {
            'admin_details': qs_admin,
        }
        if not request.user.is_authenticated:
            return redirect("administrator:admin_login")
        return render(request, 'administrator/examManagement/adminCreateExam.html', context)

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
        part = request.POST.get("part_to_delete")

        qs_exam = Exam.objects.all() #Gets all the exam in the db
        qs_parts = Part.objects.filter(exam_id = latest_exam) #Gets the parts of the latest exam added
        qs_questions = Question.objects.filter(exam = latest_exam) #Gets all the questions of the latest exam added
        part_ques_number = Question.objects.filter(part_id = part).count() #Counts the number of questions of the particular part
        
        qs_admin = Administrator.objects.filter(user_id=request.user.id)
        
        context = {
            'admin_details': qs_admin,
            'latest_exam': qs_exam,
            'parts': qs_parts,
            'questions': qs_questions,
            'part_number': part_ques_number,
        }

        if not request.user.is_authenticated:
            return redirect("administrator:admin_login")
        
        if latest_exam:
            latest_exam_id = latest_exam.pk
            get_exam = Exam.objects.filter(exam_id = latest_exam_id)

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
            
            add_part = Part(part_name = part_name, instructions = instruction, exam = get_exam_id)
            add_part.save()

            messages.success(request, "Part saved.")

        # Method to create exam questions
        elif 'btnSaveQuestion' in request.POST:
            exam_id = request.POST.get("exam_id")
            part = request.POST.get("part")
            question = request.POST.get("question")
            optionA = request.POST.get("optionA")
            optionB = request.POST.get("optionB")
            optionC = request.POST.get("optionC")
            optionD = request.POST.get("optionD")
            points = request.POST.get("points")
            answer = request.POST.get("option")

            get_exam_id = Exam.objects.get(exam_id = exam_id)
            get_part_id = Part.objects.get(part_id = part)

            count_ques_no = Question.objects.filter(part = part).count()
            question_no = count_ques_no + 1
            add_question = Question(question_no = question_no, exam = get_exam_id, part = get_part_id, question = question, optionA = optionA, optionB = optionB, 
                optionC = optionC, optionD = optionD, answer = answer, points = points)
            add_question.save()

            # Update total exam items and overall points of Exam
            total_items = Question.objects.filter(exam = get_exam_id).count()
            total_points = Question.objects.filter(exam = get_exam_id).aggregate(Sum('points')).get('points__sum')
            
            update_total_items = Exam.objects.filter(exam_id = exam_id).update(total_items = total_items)
            update_total_points = Exam.objects.filter(exam_id = exam_id).update(overall_points = total_points)

            # Update total exam items in Exam Part
            part_total_items = Question.objects.filter(part_id = part).count()
            update_part_total_items = Part.objects.filter(part_id = part).update(total_items = part_total_items)
            
            # Update overall points of the particular Exam Part
            part_overall_pts = Question.objects.filter(part = get_part_id).aggregate(Sum('points')).get('points__sum')

            update_part_overall_pts = Part.objects.filter(part_id = part).update(overall_points = part_overall_pts)
            messages.success(request, "Question saved.")
        
        # Method to delete question
        elif 'btnDelQues' in request.POST:
            ques_to_delete = request.POST.get("ques_to_delete")
            part = request.POST.get("part")

            # Deletes the question with the given question id
            del_ques = Question.objects.filter(question_id = ques_to_delete).delete()

            # Update question number after deleting of question
            count_ques_no = Question.objects.filter(part = part).count() #Counts all the questions in the selected part
            get_ques = Question.objects.filter(part = part) #Gets all questions saved in the part selected from the template

            #Loops over the questions saved under the part selected based on the primary key and
            #stores the index increased by 1 as the updated question number
            for ques_no, question in enumerate(get_ques): 
                update_ques_no = get_ques.filter(question_id = question.pk).update(question_no = ques_no+1)
            
            # Update total exam items in Exam after deleting
            get_exam = Exam.objects.last()
            total_items = Question.objects.filter(exam = get_exam).count()
            update_total_items = Exam.objects.filter(exam_id = get_exam.pk).update(total_items = total_items)

            # Update overall points (Exam) of the selected part after deleting
            exam_overall_points = Question.objects.filter(exam_id = get_exam.pk).aggregate(Sum('points')).get('points__sum')
            update_exam_overall_points = Exam.objects.filter(exam_id = get_exam.pk).update(overall_points = exam_overall_points)

            # Update total exam items in Exam Part when question is deleted
            part_total_items = Question.objects.filter(part_id = part).count()
            update_part_total_items = Part.objects.filter(part_id = part).update(total_items = part_total_items)

            # Update overall points (Part) of the selected part after deleting
            part_overall_points = Question.objects.filter(part_id = part).aggregate(Sum('points')).get('points__sum')
            update_part_pverall_points = Part.objects.filter(part_id = part).update(overall_points = part_overall_points)

            messages.success(request, "Successfully deleted question.")

        elif 'btnSaveEdited' in request.POST:
            ques_id = request.POST.get("ques_id")
            part = request.POST.get("edit_part")
            question_no = request.POST.get("edit_question_no")
            question = request.POST.get("edit_question")
            optionA = request.POST.get("edit_optionA")
            optionB = request.POST.get("edit_optionB")
            optionC = request.POST.get("edit_optionC")
            optionD = request.POST.get("edit_optionD")
            answer = request.POST.get("edit_option")
            points = request.POST.get("edit_points")

            get_part_id = Part.objects.get(part_id = part)

            edit_question = Question.objects.filter(question_id = ques_id).update(question_no = question_no, part = get_part_id, question = question, optionA = optionA, optionB = optionB, 
                optionC = optionC, optionD = optionD, answer = answer, points = points)

            # Update overall points (Exam) of the selected part after editing
            get_exam = Exam.objects.last()
            exam_overall_points = Question.objects.filter(exam_id = get_exam.pk).aggregate(Sum('points')).get('points__sum')
            update_exam_overall_points = Exam.objects.filter(exam_id = get_exam.pk).update(overall_points = exam_overall_points)
            
            # Update total exam items in Exam Part after editing
            get_parts=Part.objects.filter(exam_id = get_exam.pk)
            
            # Loops through all the items in the parts from a specified ID and automatically updates total items
            # and overall points when the part is changed.
            for idx, parts in enumerate(get_parts):
                #  Update total items of the parts after editing
                part_total_items = Question.objects.filter(part_id = parts.pk).count()
                update_part_total_items = Part.objects.filter(part_id = parts.pk).update(total_items = part_total_items)

                # Update overall points of the parts after editing
                part_overall_points = Question.objects.filter(part_id = parts.pk).aggregate(Sum('points')).get('points__sum')
                update_part_pverall_points = Part.objects.filter(part_id = parts.pk).update(overall_points = part_overall_points)

            messages.success(request, "Question edited successfully.")
        
        elif 'btnDelPart' in request.POST:
            part_to_delete = request.POST.get("part_to_delete")

            del_ques = Part.objects.filter(part_id = part_to_delete).delete()

            # Update total exam items in Exam after deleting
            get_exam = Exam.objects.last()
            total_items = Question.objects.filter(exam = get_exam).count()
            update_total_items = Exam.objects.filter(exam_id = get_exam.pk).update(total_items = total_items)

            # Update overall points in Exam after deleting
            overall_points = Question.objects.filter(exam_id = get_exam.pk).aggregate(Sum('points')).get('points__sum')
            update_exam_overall_points = Exam.objects.filter(exam_id = get_exam.pk).update(overall_points = overall_points)

            messages.success(request, "Successfully deleted part.")

        else:
            messages.error(request, "Failed to process query.")
  
        return redirect("administrator:admin_exam_details")

class AdminViewAllExamsTable(View):
    def get(self, request):
        qs_exam = Exam.objects.all()
        qs_admin = Administrator.objects.filter(user_id=request.user.id)
        
        context = {
            'admin_details': qs_admin,
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
                messages.success(request, "Successfully deleted exam.")

        return redirect("administrator:all-exams")