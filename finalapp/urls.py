from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from finalapp.views import schooladmin_logout,admin_attendance_view,schooladmin_login, admin_take_attendance_view,teacher_logout,view_feesadmin, admin_view_attendance_view, approve_teacher_job_application, enter_attendance,    reject_teacher_job_application, save_attendance,   teacher_job_application, teacher_job_application_success, view_attendance, view_student_admission_requests_table,approve_student_admission, reject_student_admission, student_admission_request, student_admission_request_success, view_student_admission_requests, view_student_leave_requests_table,student_leave_request,student_leave_request_success,view_student_leave_requests,approve_student_leave, reject_student_leave,view_leave_requests_table,leave_request, leave_request_success, view_leave_requests, approve_leave, reject_leave,student_register,student_login,total_count,overview,teacher_total,base,chart_view,add_notice,add_course,add_subject,add_student,add_teacher,return_view,dashboard,add_teacher_details, student_list,order,cancel_view, attendance_list, course_list, subject_list, take_attendance, update_fee, upload_results,view_fees, home,aboutus,contactus,details_list, notice_list,teacher_job_list,success,submit_teacher_feedback,teacher_feedback_list,submit_feedback,student_feedback_list,otp,teacher_login,add_student_details,teacher_register,studentdata,teacherdata,teacher_page,student_page,send_email, upload_answer_sheet, upload_question_paper, view_answer_sheets, view_question_papers, view_results, view_teacher_job_applications, view_teacher_job_applications_table
app_name="finalapp"
urlpatterns =[

    path('student_login/',student_login,name='student_login'),

    path('student_register/',student_register,name='student_register'),

    path('overview/',overview,name='overView'),
    path('total_count/', total_count, name='total_count'),
    path('teacher_total/',teacher_total,name='teacher_total'),
    path('base/',base,name="base"),
    #path('teacher_dashboard/',teacher_dashboard,name="teacher_dashboard"),
    path('chart/', chart_view, name='chart_view'),
    path('',home,name='home'),
    path('c/',contactus,name='contactus'),
    path('a/',aboutus,name='aboutus'),
    path('success/', success, name='success'),
    path('tp/',teacher_page,name='teacher_page'),
    path('sp/',student_page,name='student_page'),
    path('tr/',teacher_register,name='teacher_register'),
    path('sd/',studentdata,name='studentdata'),
    path('td/',teacherdata,name='teacherdata'),
    path('sa/',add_student_details,name='add_student_details'),
    path('ta/',add_teacher_details,name='add_teacher_details'),
    path('mail/',send_email,name='send_email'),
    path('tl/',teacher_login,name='teacher_login'),
    path('otp/<str:otp>/<str:username>/<str:password>/<str:email>/',otp,name='otp'),
    path('submit_feedback/',submit_feedback,name='submit_feedback'),
    path('feedback_list/',student_feedback_list,name='student_feedback_list'),
    path('submit_teacher_feedback/',submit_teacher_feedback,name='submit_teacher_feedback'),
    path('teacher_feedback_list/',teacher_feedback_list,name='teacher_feedback_list'),
     #student leave
    path('student_leave_request/', student_leave_request, name='student_leave_request'),
    path('student_leave_request/success/', student_leave_request_success, name='student_leave_request_success'),
    path('view_student_leave_requests/', view_student_leave_requests, name='view_student_leave_requests'),
    path('approve_student_leave/<int:leave_id>/', approve_student_leave, name='approve_student_leave'),
    path('reject_student_leave/<int:leave_id>/', reject_student_leave, name='reject_student_leave'),
    path('view_student_leave_requests_table/', view_student_leave_requests_table, name='view_student_leave_requests_table'),

     #Teacher Leave
    path('leave_request/', leave_request, name='leave_request'),
    path('leave_request/success/', leave_request_success, name='leave_request_success'),
    path('view_leave_requests/', view_leave_requests, name='view_leave_requests'),
    path('approve_leave/<int:leave_id>/', approve_leave, name='approve_leave'),
    path('reject_leave/<int:leave_id>/', reject_leave, name='reject_leave'),
    path('view_leave_requests_table/', view_leave_requests_table, name='view_leave_requests_table'),
     
     #Admission Form
    path('student_admission_request/', student_admission_request, name='student_admission_request'),
    path('student_admission_request_success/', student_admission_request_success, name='student_admission_request_success'),
    path('view_student_admission_requests/', view_student_admission_requests, name='view_student_admission_requests'),
    path('approve_student_admission/<int:admission_id>/', approve_student_admission, name='approve_student_admission'),
    path('reject_student_admission/<int:admission_id>/', reject_student_admission, name='reject_student_admission'),
    path('view_student_admission_requests_table/', view_student_admission_requests_table, name='view_student_admission_requests_table'),

    #Teacher Job 
    path('teacher_job_application/', teacher_job_application, name='teacher_job_application'),
    path('teacher_job_application/success/', teacher_job_application_success, name='teacher_job_application_success'),
    path('view_teacher_job_applications/', view_teacher_job_applications, name='view_teacher_job_applications'),
    path('approve_teacher_job_application/<int:job_id>/', approve_teacher_job_application, name='approve_teacher_job_application'),
    path('reject_teacher_job_application/<int:job_id>/', reject_teacher_job_application, name='reject_teacher_job_application'),
    path('job-list/', teacher_job_list, name='teacher_job_list'),
    path('view_teacher_job_applications_table/', view_teacher_job_applications_table, name='view_teacher_job_applications_table'),



    path('details_list/',details_list,name='details_list'),
    path('notice-list/', notice_list, name='notice_list'),
    path('add/', add_notice, name='add_notice'),
    path('upload-question-paper/', upload_question_paper, name='upload_question_paper'),
    path('upload-answer-sheet/', upload_answer_sheet, name='upload_answer_sheet'),
    path('view-question-papers/', view_question_papers, name='view_question_papers'),
    path('view-answer-sheets/', view_answer_sheets, name='view_answer_sheets'),
    path('update-fee/',update_fee,name='update_fee'),
    path('view_fee/',view_fees,name='view_fees'),
    path('view_feeadmin/',view_feesadmin,name='view_feesadmin'),
    path('courses/', course_list, name='course_list'),
    path('subjects/', subject_list, name='subject_list'),
    path('take-attendance/', take_attendance, name='take_attendance'),
    path('attendance-list/', attendance_list, name='attendance_list'),
    path('upload_results/', upload_results, name='upload_results'),
    path('view_results/', view_results, name='view_results'),
    path('view/', return_view, name='return_view'),
    path('cancel/',cancel_view, name='cancel_view'),
    path('order/',order,name='order'),
    path('total/',student_list,name='student_list'),
    path('dashboard/',dashboard,name='dashboard'),
    path('schooladmin_logout/', schooladmin_logout, name='schooladmin_logout'),

    path('add_teacher/', add_teacher, name='add_teacher'),
    path('add_student/', add_student, name='add_student'),
    path('add_course/', add_course, name='add_course'),
    path('add_subject/', add_subject, name='add_subject'),


    path('admin-attendance/', admin_attendance_view,name='admin-attendance'),
    path('admin-take-attendance/<str:Co>/', admin_take_attendance_view,name='admin-take-attendance'),
    path('admin-view-attendance/<str:student>/', admin_view_attendance_view,name='admin-view-attendance'),
    path('enter-attendance/', enter_attendance, name='enter_attendance'),
    path('view_attendance/', view_attendance, name='view_attendance'),
    path('save_attendance/', save_attendance, name='save_attendance'),
    path('teacher_logout/', teacher_logout, name='teacher_logout'),
    path('schooladmin_login/', schooladmin_login, name='schooladmin_login'),
   

    
     

     
     



     
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
          

     