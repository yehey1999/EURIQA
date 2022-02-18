from cmath import nan
from django.http import Http404, HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from enrollee.models import *
from administrator.models import *
from django.core.files.storage import FileSystemStorage

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
    
    def post(self, request):
        if request.method == 'POST':
            if 'btnNext' in request.POST:
                picture = request.FILES['picture']
                fileSystemStorage = FileSystemStorage()
                filename = fileSystemStorage.save(picture.name, picture)
                picture = fileSystemStorage.url(filename)
                update_picture = Enrollee.objects.filter(user_id = request.user.id).update(pictures = picture)
            return redirect("enrollee:enrollee_frtest")

class EnrolleeFaceRecTest(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("enrollee:enrollee_login")
        return render(request, 'enrollee/enrolleFaceRecTest.html')
       
class EnrolleeInstructionsView(View):
    def get(self, request):
        if request.user.is_authenticated:
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
            return render(request, 'enrollee/enrolleeInstructions.html', context)

        else:
            return redirect("enrollee:enrollee_login")

def exam_page(request, exam_id=None, part_id=None):
    # Make sure the users are logged in 
    if request.user.is_authenticated:
        if request.method != 'POST':
            # Make sure the examinee is not done taking the exam before redirecting to exam page
            get_exam_status = Enrollee.objects.filter(user = request.user.id).values_list('exam_status', flat=True)
            exam_is_done = Enrollee.objects.filter(user = request.user.id).get(exam_status__in = get_exam_status)

            if exam_is_done.exam_status == 'not done':
                # Check level of enrollee
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

                qs_all_parts = Part.objects.filter(exam = exam_id)
                qs_part = Part.objects.filter(part_id = part_id)
                qs_question = Question.objects.filter(exam_id = exam_id).filter(part = part_id)
                qs_question_no = qs_question.values_list('question_no', flat=True)
                
                get_last_part = Part.objects.last()

                context = {
                    'exams': qs_exam,
                    'parts': qs_part,
                    'all_parts': qs_all_parts,
                    'questions': qs_question,
                    'question_no': qs_question_no,
                    'last_part': get_last_part,
                }

                return render(request, 'enrollee/enrolleeExam.html', context)
            
            else:
                messages.error(request,"You are already done taking the exam.")
                return redirect("enrollee:enrollee_instructions")
                

        else:
            if 'btnSubmitExam' in request.POST:
                # Get question number to append to the answer variable to get all their data from the template
                qs_question_no = Question.objects.filter(exam_id = exam_id).filter(part = part_id).values_list('question_no', flat=True)      
                
                qs_question_id = Question.objects.filter(exam_id = exam_id).filter(part = part_id).values_list('question_id')
                qs_answers = Question.objects.filter(question_id__in = qs_question_id).values_list('answer')
                
                # Get question ids of the exam. This will be used to get the Question instances of each questions from the exam.
                # We need the Question instances for ExamResults has a foreign key field from the Question. 
                get_ques = Question.objects.filter(exam = exam_id).filter(part = part_id).values_list('question_id', flat=True)
                
                # Declare two lists that will receive the answers and the question ids.
                list_answers = []
                list_ques_id = []
                list_correct_ans = []
                # Gets the id of the currently logged in enrollee
                enrollee = request.user.id

                # Get enrollee instance based from the enrollee id
                get_enrollee = Enrollee.objects.get(user_id = enrollee)
                
                # Get exam instance based from the exam id
                get_exam = Exam.objects.get(exam_id = exam_id)

                # Get part instance based from the part id
                get_part = Part.objects.get(part_id = part_id)
                
                # Loop over all the question numbers of their respective parts in the exam
                for idx, num in enumerate(qs_question_no):
                    # The name of the template field for all the answers of the enrollee is "[answer]+[question number]"
                    ques_num="answer"+str(num)

                    # Retrieves all the answers inputted by the enrollee
                    answer = request.POST.get(ques_num)

                    # Stores the retrieved answer from the exam in a list.
                    list_answers.append(answer)
                
                # Loop over all the question records to get their respective instances.
                for ques in Question.objects.filter(question_id__in=get_ques):
                    ques_id = Question.objects.get(question_id = ques.pk)

                    # Store the question instances in the list_ques_id.
                    list_ques_id.append(ques_id)
                    # Store the correct answers in the list_correct_ans.
                    list_correct_ans.append(ques.answer)

                    try: 
                        # Loop over the list of ques_id to save each inputs from the enrollee to the database.
                        # Since both lists of question id and answer will always have the same number of itemss,
                        # we get the index from one of them to allow easy record saving.
                        for i in range(len(list_ques_id)):
                            save_items = ExamAnswers(enrollee = get_enrollee, exam = get_exam, part = get_part, is_correct=True, question = list_ques_id[i], answer = list_answers[i])
                        save_items.save()

                        if(list_correct_ans[i] == list_answers[i]):
                            save_items = ExamAnswers.objects.filter(question_id = list_ques_id[i]).update(is_correct=True)
                        else:
                            save_items = ExamAnswers.objects.filter(question_id = list_ques_id[i]).update(is_correct=False)

                    # When IntegrityError occurs, just update the database with the same values.
                    except:
                        for i in range(len(list_ques_id)):
                            if(list_correct_ans[i] == list_answers[i]):
                                save_items = ExamAnswers.objects.filter(question_id = list_ques_id[i]).update(is_correct=True)
                            else:
                                save_items = ExamAnswers.objects.filter(question_id = list_ques_id[i]).update(is_correct=False)

                # Get the exam score by counting is_correct
                get_answers = ExamAnswers.objects.filter(exam_id = exam_id)
                get_exam_score = get_answers.filter(is_correct = True).count()

                # Save/Update Results of Exam for each Part
                new_results, save_results = ExamResults.objects.update_or_create(enrollee = get_enrollee, exam = get_exam, defaults={'total_score': get_exam_score})

                # Get all part IDs and save it in a list
                get_all = Part.objects.filter(exam_id = exam_id).values_list('part_id', flat=True)
                part_list=list(get_all)
                
                # Append Nonetype at list to serve as stopper when looping through the part ids
                part_list.append(None)

                # Get the ID of the last Part
                last_part = Part.objects.filter(exam_id = exam_id).last()
                
                # Loop over the part ids to properly configure the URLs
                for i in range(len(part_list)):
                    if part_list[i] == part_id or part_list[i-1] != part_id:
                        pass
                        
                    elif (part_list[i] is not None) and (part_list[i] <= last_part.pk or part_list[i] >= last_part.pk):
                        return redirect("enrollee:enrollee_exam", exam_id = exam_id, part_id = part_list[i])
                    else:
                        # Update exam status of enrollee if final part is already answered
                        update_status = Enrollee.objects.filter(user = request.user.id).update(exam_status = "done")
                        return redirect("enrollee:enrollee_examcompletion", enrollee_id=request.user.id, exam_id = exam_id)

def exam_results(request, enrollee_id=None, exam_id=None):
    if request.user.is_authenticated:
        if request.method != 'POST':
            qs_results = ExamResults.objects.filter(exam_id = exam_id)
            qs_exams = Exam.objects.filter(exam_id= exam_id)
            qs_parts = Part.objects.filter(exam = exam_id)
            
            # Get the overall_points value from Exam
            get_exam = Exam.objects.get(exam_id = exam_id)
            total_points = get_exam.overall_points

            # Get the total_score value from ExamResults
            get_results = ExamResults.objects.get(exam_id = exam_id)
            score = get_results.total_score
            
            # Get the passing score (60% passing rate)
            passing_score = total_points*0.60

            # Check if student passed 
            if score >= passing_score:
                status = "passed"
            
            else:
                status = "failed"

            score_list = []

            for qs in qs_parts:
                correct_answers_per_part = ExamAnswers.objects.filter(exam_id = exam_id).filter(part_id=qs.pk).filter(is_correct=True)
                score_per_part = correct_answers_per_part.count()
                score_list.append(score_per_part)
            
            # Zip the Part objects and the scores for easy displaying in templates
            parts_and_score = zip(qs_parts, score_list)
            
            context={
                'results' : qs_results,
                'exams': qs_exams,
                'status': status,
                'score_list': score_list,
                'parts_and_score': parts_and_score,
            }
            return render(request, 'enrollee/enrolleeExamCompletion.html', context)

