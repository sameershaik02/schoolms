from email.message import EmailMessage
import uuid
from django import forms
from django.shortcuts import render,redirect
from finalapp.finalapp import fee_id, get_fee, total_
from finalapp.models import Teacher,Student,TeacherJob,Userdata,Userdata1,StudentFeedback,TeacherFeedback,StudentLeave,TeacherLeave
from finalapp.forms import Userform,Userform1,StudentFeedbackForm,TeacherFeedbackForm,StudentLeaveForm,ContactForm
from django.http import HttpResponse,HttpResponseRedirect,BadHeaderError
from finalapp.school import *
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.core.mail import send_mail
from finalapp.models import Student,Teacher,TeacherJob
import random
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from finalapp.models import ExcelFile
from finalapp.forms import ExcelFileForm
from finalapp import models

# Create your views here.
def base(request):
    return render(request,'mainapp/base.html')
def home(request):
    return render(request,'home.html')
def contactus(request):
    return render(request,'contactus.html')
def aboutus(request):
    return render(request,'aboutus.html')
def courses(request):
    return render(request,'courses.html')
def teacher_page(request):
    t = Teacher.objects.all()
    return render(request,'teacher_page.html',{'t':t})
@login_required
def student_page(request):
    s = Student.objects.all()
    return render(request,'student_page.html',{'s':s})


def studentdata(request):
    data=Userdata1.objects.all()
    return render(request,"studentdata.html",{'d':data})
def teacherdata(request):
    data=Userdata.objects.all()
    return render(request,"teacherdata.html",{'k':data})
def add_student_details(request):
    if request.method=="POST" and request.POST.get('delete')=='Delete':
        Firstname=request.POST.get('Firstname')
        sd=Student.objects.get(id=Firstname)
        sd.delete()
    c=get_student(request)
    context={'c':c}
    return render(request,'add_student_details.html',context)

from .forms import StudentData, StudentForm

def add_student(request):
    if request.method == 'POST':
        form = StudentData(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('finalapp:success')  # Redirect to a success page
    else:
        form = StudentData()

    return render(request, 'add_student.html', {'form': form})
    
def add_teacher_details(request):
    if request.method=="POST" and request.POST.get('delete')=='Delete':
        Firstname=request.POST.get('Firstname')
        td=Teacher.objects.get(id=Firstname)
        td.delete()
    d=get_teacher(request)
    context={'d':d}
    return render(request,'add_teacher_details.html',context)

def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finalapp:success')  # Redirect to a success page
    else:
        form = TeacherForm()

    return render(request, 'add_teacher.html', {'form': form})



def details_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'details_list.html', {'teachers': teachers})

# def add_teacher_details(request):
#     if request.method=="POST" and request.POST.get('delete')=='Delete':
#         Lastname=request.POST.get('Lastname')
#         st=Teacher.objects.get(id=Lastname)
#         st.delete()
#     r=get_teacher(request)
#     context={'r':r}
#     return render(request,'add_teacher_details.html',context)

def student_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('finalapp:student_page')  # Change the redirection URL to your desired home page
        else:
            messages.info(request, 'Invalid user credentials')
            return redirect('finalapp:student_login')
    else:
        return render(request, 'student_login.html')

def student_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pass1']
        password2 = request.POST['pass2']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('finalapp:student_register')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        messages.success(request, 'Registration successful. Please log in.')
        return redirect('finalapp:student_login')
    else:
        return render(request, 'student_register.html')



def teacher_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('finalapp:teacher_page')
        else:
            messages.info(request,'Invalid user credentials')
            return redirect('finalapp:teacher_login')
    else:
        return render(request,'teacher_login.html')
def teacher_logout(request):
    auth.logout(request)
    return redirect('finalapp:home') 
def teacher_dashboard(request):
    return render(request,'teacher_dashboard.html')
def send_otp(email,otp):
    subject="OTP Verification"
    message=f'Your OTP for registration is: {otp}'
    send_mail(subject,message,None,[email])

def teacher_register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['pass1']
        password2=request.POST['pass2']
        if User.objects.filter(username=username).exists():
            messages.info(request,"Username already taken")
            return redirect('finalapp:teacher_register')
        otp_number=random.randint(1000,9999)
        otp=str(otp_number)
        send_otp(email,otp)
        request.session['username']=username
        request.session['email']=email
        request.session['password']=password
        request.session['password2']=password2
        request.session['otp']=otp 
        return HttpResponseRedirect(reverse('finalapp:otp',args=[otp,username,password,email]))
    else:
        return render(request,'teacher_register.html')













    

def otp(request,otp,username,password,email):
    if request.method=="POST":
        uotp=request.POST['uotp']
        otp_from_session=request.session.get('otp')

        if uotp==otp_from_session:
            username=request.session.get('username')
            email=request.session.get('email')
            password=request.session.get('password')
            user=User.objects.create_user(username=username,password=password,email=email)
            user.save()
            return redirect('finalapp:teacher_login')
        else:
            messages.error(request,'Invalid OTP')
            return redirect('finalapp:otp',otp=otp,username=username,password=password,email=email)
    return render(request,'otp.html',{'otp':otp ,'username':username,'password':password,'email':email})
        


        




def send_email(request):
    subject = request.POST.get("subject", "Confirmation mail")
    message = request.POST.get("message", "otp is 25312")
    from_email = request.POST.get("from_email", "tksiva05@gmail.com")
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ["tksiva05@gmail.com"])
        except BadHeaderError:
            return HttpResponse("Invalid header found.")
        return HttpResponseRedirect("Mail sent successfully.")
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse("Make sure all fields are entered and valid.")




def student_feedback_list(request):
    feedback_list = StudentFeedback.objects.all()
    return render(request, 'feedback_list.html', {'feedback_list': feedback_list})

def submit_feedback(request):
    if request.method == 'POST':
        form = StudentFeedbackForm(request.POST)
        if form.is_valid():
            # Get the currently logged-in user
            user = request.user

            # Check if the user has a related Teacher profile
            try:
                student = user.student
            except Student.DoesNotExist:
                # If the Teacher profile doesn't exist, create it
                student = Student.objects.create(user=user)

            feedback = form.save(commit=False)
            feedback.student = student
            feedback.save()

            return redirect('finalapp:success')
    else:
        form = StudentFeedbackForm()

    return render(request, 'submit_feedback.html', {'form': form})


def teacher_feedback_list(request):
    feedback_list = TeacherFeedback.objects.all()
    return render(request, 'teacher_feedback_list.html', {'feedback_list': feedback_list})

def submit_teacher_feedback(request):
    if request.method == 'POST':
        form = TeacherFeedbackForm(request.POST)
        if form.is_valid():
            # Get the currently logged-in user
            user = request.user

            # Check if the user has a related Teacher profile
            try:
                teacher = user.teacher
            except Teacher.DoesNotExist:
                # If the Teacher profile doesn't exist, create it
                teacher = Teacher.objects.create(user=user)

            feedback = form.save(commit=False)
            feedback.teacher = teacher
            feedback.save()

            return redirect('finalapp:success')
    else:
        form = TeacherFeedbackForm()

    return render(request, 'submit_teacher_feedback.html', {'form': form})



# Student Leave

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import StudentLeave
from .forms import StudentLeaveForm

def student_leave_request(request):
    if request.method == 'POST':
        form = StudentLeaveForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.save()
            return redirect('finalapp:student_leave_request_success')
    else:
        form = StudentLeaveForm()

    return render(request, 'student_leave_requests.html', {'form': form})

def student_leave_request_success(request):
    return render(request, 'student_leave_request_success.html')

def view_student_leave_requests(request):
    leave_requests = StudentLeave.objects.all()
    return render(request, 'view_student_leave_requests.html', {'leave_requests': leave_requests})

def approve_student_leave(request, leave_id):
    leave_request = StudentLeave.objects.get(pk=leave_id)
    leave_request.is_approved = True
    leave_request.save()
    return redirect('finalapp:view_student_leave_requests')

def reject_student_leave(request, leave_id):
    leave_request = StudentLeave.objects.get(pk=leave_id)
    leave_request.is_approved = False
    leave_request.save()
    return redirect('finalapp:view_student_leave_requests')
def view_student_leave_requests_table(request):
    leave_requests = StudentLeave.objects.all()
    return render(request, 'view_student_leave_requests_table.html', {'leave_requests': leave_requests})

#Teacher Leave

from django.shortcuts import render, redirect
from .models import TeacherLeave
from .forms import LeaveRequestForm

def leave_request(request):
    if request.method == 'POST':
        print('-----------------------------------------------------------')
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.save()
            return redirect('finalapp:leave_request_success')  # Redirect to a success page
        else:
            print(form.errors) 
    else:
        form = LeaveRequestForm()    

    return render(request, 'leave_request.html', {'form': form})

def leave_request_success(request):
    return render(request, 'leave_request_success.html')

def view_leave_requests(request):
    leave_requests = TeacherLeave.objects.all()
    return render(request, 'view_leave_requests.html', {'leave_requests': leave_requests})

def approve_leave(request, leave_id):
    leave_request = TeacherLeave.objects.get(pk=leave_id)
    leave_request.is_approved = True
    leave_request.save()
    return redirect('finalapp:view_leave_requests')

def reject_leave(request, leave_id):
    leave_request = TeacherLeave.objects.get(pk=leave_id)
    leave_request.is_approved = False
    leave_request.save()
    return redirect('finalapp:view_leave_requests')

def view_leave_requests_table(request):
    leave_requests = TeacherLeave.objects.all()
    return render(request, 'view_leave_requests_table.html', {'leave_requests': leave_requests})


#Contact Us

def contactus(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'success.html')  # Redirect to a success page
    else:
        form = ContactForm()

    return render(request, 'contactus.html', {'form': form})
#Success html

def success(request):
    return render(request, 'success.html')
#Admission Form
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import StudentAdmission, StudentForm
from .forms import StudentAdmissionRequestForm

@login_required
def student_admission_request(request):
    if request.method == 'POST':
        form = StudentAdmissionRequestForm(request.POST)
        if form.is_valid():
            student_form = form.save()

            # Create a corresponding StudentAdmission instance
            admission_request = StudentAdmission.objects.create(student_form=student_form)
            
            return redirect('finalapp:student_admission_request_success')
        print('---------------------',form.errors)
    else:
        form = StudentAdmissionRequestForm()

    return render(request, 'student_admission_request.html', {'form': form})
def student_admission_request_success(request):
    return render(request, 'student_admission_request_success.html')

def view_student_admission_requests(request):
    admission_requests = StudentAdmission.objects.all()
    return render(request, 'view_student_admission_requests.html', {'admission_requests': admission_requests})

def approve_student_admission(request, admission_id):
    admission_request = StudentAdmission.objects.get(pk=admission_id)
    admission_request.is_approved = True
    admission_request.save()
    return redirect('finalapp:view_student_admission_requests')


def reject_student_admission(request, admission_id):
    admission_request = StudentAdmission.objects.get(pk=admission_id)
    admission_request.is_approved = False
    admission_request.save()
    return redirect('finalapp:view_student_admission_requests')

def view_student_admission_requests_table(request):
    admission_requests = StudentAdmission.objects.all()
    return render(request, 'view_student_admission_requests_table.html', {'admission_requests': admission_requests})

#Teacher Job Application
# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TeacherJob
from .forms import TeacherJobApplicationForm


def teacher_job_application(request):
    if request.method == 'POST':
        form = TeacherJobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            job_application = form.save()
            return redirect('finalapp:teacher_job_application_success')
    else:
        form = TeacherJobApplicationForm()

    return render(request, 'teacher_job_application.html', {'form': form})


def teacher_job_application_success(request):
    return render(request, 'teacher_job_application_success.html')


def view_teacher_job_applications(request):
    job_applications = TeacherJob.objects.all()
    return render(request, 'view_teacher_job_applications.html', {'job_applications': job_applications})



def approve_teacher_job_application(request, job_id):
    job_application = TeacherJob.objects.get(pk=job_id)
    job_application.status = 'ACCEPTED'
    job_application.save()
    return redirect('finalapp:view_teacher_job_applications')
def reject_teacher_job_application(request, job_id):
    job_application = get_object_or_404(TeacherJob, pk=job_id)

    # Assuming that you want to set the status to 'REJECTED' when rejecting the job application
    job_application.status = 'REJECTED'
    job_application.save()

    return redirect('finalapp:view_teacher_job_applications')
def view_teacher_job_applications_table(request):
    job_applications = TeacherJob.objects.all()
    return render(request, 'view_teacher_job_applications_table.html', {'job_applications': job_applications})


from .models import Attendance, Fee, Notice, Payment, Result, Subject
from .forms import AttendanceForm, FeeUpdateForm, NoticeForm, ResultForm, TeacherForm

def notice_list(request):
    notices = Notice.objects.all()
    return render(request, 'notice_list.html', {'notices': notices})

def add_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            admin_user, created = User.objects.get_or_create(username='admin')
            if created:
                admin_user.set_password('admin')  # Set the password
                admin_user.save()

            notice.author = admin_user
            notice.save()
            return redirect('finalapp:success')
    else:
        form = NoticeForm()
    return render(request, 'add_notice.html', {'form': form})
'''def add_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)

            # Check if the entered username and password match the fixed values
            fixed_username = 'admin'
            fixed_password = 'admin@1'
            if (request.user.username == fixed_username and request.user.check_password(fixed_password)):
                notice.author = request.user
                notice.save()
                return redirect('finalapp:success')
            else:
                # Handle the case where entered values don't match
                messages.error(request, 'Invalid username or password')
    else:
        form = NoticeForm()

    return render(request, 'add_notice.html', {'form': form})'''



from .models import QuestionPaper, AnswerSheet
from .forms import QuestionPaperUploadForm, AnswerSheetUploadForm
def upload_question_paper(request):
    if request.method == 'POST':
        form = QuestionPaperUploadForm(request.POST, request.FILES)
        if form.is_valid():
            question_paper = form.save(commit=False)
            question_paper.uploaded_by = request.user
            question_paper.save()
            return redirect('finalapp:success')
    else:
        form = QuestionPaperUploadForm()
    return render(request, 'upload_question_paper.html', {'form': form})



def upload_answer_sheet(request):
    if request.method == 'POST':
        form = AnswerSheetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            answer_sheet = form.save(commit=False)
            answer_sheet.student = request.user
            answer_sheet.save()
            return redirect('finalapp:success')
    else:
        form = AnswerSheetUploadForm()
    return render(request, 'upload_answer_sheet.html', {'form': form})

def view_question_papers(request):
    question_papers = QuestionPaper.objects.all()
    return render(request, 'view_question_papers.html', {'question_papers': question_papers})

def view_answer_sheets(request):
    answer_sheets = AnswerSheet.objects.filter(student=request.user)
    return render(request, 'view_answer_sheets.html', {'answer_sheets': answer_sheets})

def update_fee(request):
    if request.method == 'POST':
        form = FeeUpdateForm(request.POST)
        if form.is_valid():
            fee = form.save(commit=False)
            fee.student = request.user
            fee.updated_by = request.user
            fee.save()
            return redirect('finalapp:view_feesadmin')
    else:
        form = FeeUpdateForm()
    return render(request, 'update_fee.html', {'form': form})

'''def update_fee(request, fee_id):
    fee = get_object_or_404(Fee, id=fee_id)

    if request.method == 'POST':
        form = FeeUpdateForm(request.POST, instance=fee)
        if form.is_valid():
            updated_fee = form.save(commit=False)
            updated_fee.student = request.user
            updated_fee.updated_by = request.user
            updated_fee.save()
            return redirect('finalapp:view_feesadmin')
    else:
        form = FeeUpdateForm(instance=fee)

    return render(request, 'update_fee.html', {'form': form}) '''  

def view_feesadmin(request):
    fees = Fee.objects.all()
    return render(request, 'view_feesadmin.html', {'fees': fees})  

def view_fees(request):
    fees = Fee.objects.all()
    return render(request, 'view_fees.html', {'fees': fees})



from django.shortcuts import render, get_object_or_404, redirect
from .models import Course
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

# views.py
from django.shortcuts import render, redirect
from .forms import CourseForm

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finalapp:success')  # Redirect to a success page
    else:
        form = CourseForm()

    return render(request, 'add_course.html', {'form': form})


def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subject_list.html', {'subjects': subjects})

from .forms import SubjectForm

def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finalapp:success')  # Redirect to a success page
    else:
        form = SubjectForm()

    return render(request, 'add_subject.html', {'form': form})
#Attendance
def take_attendance(request):
    students = Student.objects.all()
    if request.method == 'POST':
        # Set the teacher field before saving the form
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.teacher = request.user  # Set the teacher field
            attendance.save()
            return redirect('finalapp:success')
    else:
        form = AttendanceForm()
    return render(request, 'take_attendance.html', {'form': form, 'students': students})
def attendance_list(request):
    attendances = Attendance.objects.all()
    return render(request, 'attendance_list.html', {'attendances': attendances})

def student_list(request):
    students = Student.objects.all()
    student_present_days = [(student, student.total_present_days()) for student in students]

    return render(request, 'student_list.html', {'student_present_days': student_present_days})

def upload_results(request):
    if request.method == 'POST':
        form = ResultForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('finalapp:success')  # Redirect to a success page
    else:
        form = ResultForm()
    return render(request, 'upload_results.html', {'form': form})



def view_results(request):
    results = Result.objects.all()
    return render(request, 'view_results.html', {'results': results})


def order(request):
    # What you want the button to do.
    items=get_fee(request)
    for i in items:
        b=Payment(fee=i.fee,price=i.price)
        b.save()
    paypal_dict = {
        "business":"sb-ojhpc27297225@business.example.com",
        "amount": total_(request),
        "item_name": fee_id(request),
        "invoice": str(uuid.uuid4()),
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('finalapp:return_view')),
        "cancel_return": request.build_absolute_uri(reverse('finalapp:cancel_view')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form,"items":items,"total":total_(request)}
    return render(request, "order.html", context)
def return_view(request):
    return render(request,"return_view.html")
def cancel_view(request):
    return render(request,"cancel_view.html")



def index(request):
    return render(request,'index.html')


def dashboard(request):
    student_count = Student.objects.count()
    teacher_count = Teacher.objects.count()
    course_count = Course.objects.count()
    subject_count=Subject.objects.count()

    context = {
        'student_count': student_count,
        'teacher_count': teacher_count,
        'course_count': course_count,
        'subject_count': subject_count,

    }

    return render(request, 'dashboard.html', context)

def chart_view(request):
    students = Student.objects.all()
    present_days = [student.total_present_days() for student in students]

    context = {
        'students': students,
        'present_days': present_days,
    }

    return render(request, 'mainapp/chart_template.html', context)


#=============================================== admin login
def schooladmin_login(request):
    if request.method == 'POST':
        entered_username = request.POST['username']
        entered_password = request.POST['password']

        # Check if the entered username and password match the fixed values
        fixed_username = 'admin'
        fixed_password = 'admin'

        if entered_username == fixed_username and entered_password == fixed_password:
            # Redirect to the desired page upon successful login
            return redirect('finalapp:dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('finalapp:schooladmin_login')
   
    return render(request, 'admin_login.html')

def schooladmin_logout(request):
    return redirect('finalapp:home')

# views.py
from django.shortcuts import render, get_object_or_404
from .models import TeacherJob

def teacher_job_list(request):
    teacher_jobs = TeacherJob.objects.all()
    return render(request, 'teacher_job_list.html', {'teacher_jobs': teacher_jobs})
def teacher_total(request):
    teachers = Teacher.objects.all()
    total_teachers = Teacher.total_teachers()

    context = {
        'teachers': teachers,
        'total_teachers': total_teachers,
    }

    return render(request, 'teachers_total.html', context)

def total_count(request):
    total_teachers = Teacher.total_teachers()
    total_students = Student.total_students()

    context = {
        'total_teachers': total_teachers,
        'total_students': total_students,
    }

    return render(request, 'mainapp/total_count.html', context)
def overview(request):
    total_teachers = 30  # Replace with actual data
    total_students = 150  # Replace with actual data
    students = [{'Firstname': 'John'}, {'Firstname': 'Jane'}, {'Firstname': 'Doe'}]
    present_days = [10, 15, 8]  # Replace with actual data

    print("Total Teachers:", total_teachers)
    print("Total Students:", total_students)
    print("Students:", students)
    print("Present Days:", present_days)

    return render(request, 'mainapp/charts_template.html', {
        'total_teachers': total_teachers,
        'total_students': total_students,
        'students': students,
        'present_days': present_days,
    })

from django.shortcuts import render, redirect
from finalapp.forms import AskDateForm, AttendanceForm,DateSelectionForm
from finalapp.models import Attendance, Student,Course
from datetime import datetime

def admin_attendance_view(request):
    classes = Course.objects.all()
    print(classes)
    for class_instance in classes:
        print(class_instance)
    return render(request, 'admin_attendance.html',{"classes":classes})

def admin_take_attendance_view(request, Co):
    if request.method == 'POST':
        form = ExcelFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('sucess')
    else:
        form = ExcelFileForm()

    return render(request, 'upload_excel.html', {'form': form})

# Import necessary modules

# views.py
from django.shortcuts import render, redirect
from .models import Attendance, Student
from .forms import AttendanceForm

def enter_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finalapp:enter_attendance')  # Redirect to the main page after submission
    else:
        form = AttendanceForm()

    students = Student.objects.filter(Co='class1')  # Replace 'MSDS' with the desired course
    context = {'form': form, 'students': students}
    return render(request, 'enter_attendance.html', context)


from django.http import Http404

def view_attendance(request):
    excel_files = ExcelFile.objects.all()
    return render(request, 'view_attendance.html', {'excel_files': excel_files})


from finalapp.school import get_student_by_id
from django.shortcuts import render, HttpResponseRedirect
from django.utils import timezone
from .models import Attendance, Student

def save_attendance(request):
    if request.method == 'POST':
        selected_date = request.POST.get('attendance_date')  # Assuming you have a field named 'attendance_date' in your form
        for key, value in request.POST.items():
            if key.startswith('attendance_'):
                student_id = key.replace('attendance_', '')

                # Check if the student_id is a valid integer
                if not student_id.isdigit():
                    # Handle the case where the extracted student_id is not a valid integer
                    # You might want to log this or redirect to an error page
                    continue

                # Get the student by ID
                try:
                    student = Student.objects.get(pk=int(student_id))
                except Student.DoesNotExist:
                    # Handle the case where the student with the given ID does not exist
                    # You might want to log this or redirect to an error page
                    continue

                attendance_status = value

                # Save the attendance record with the selected date
                Attendance.objects.create(
                    student=student,
                    date=selected_date,
                    is_present=(attendance_status == 'on')
                )

        # Redirect to a success page or the attendance view
        return redirect('finalapp:success')
    else:
        # Handle GET request if needed
        pass

from django.shortcuts import render, get_object_or_404
from .models import Student, Attendance
from .forms import AskDateForm  # Import your AskDateForm or adjust the import statement accordingly

def admin_view_attendance_view(request, student):
    excel_files = ExcelFile.objects.all()
    return render(request, 'view_attendance.html', {'excel_files': excel_files})

# views.py


    
