from django import forms
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Teacher(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Firstname = models.CharField(max_length=120)
    Lastname = models.CharField(max_length=120)
    Email = models.EmailField(max_length=50, unique=True)
    Gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    Password = models.CharField(max_length=20)
    Address = models.TextField()
    Subject = models.CharField(max_length=20)

    def __str__(self):
        return self.Firstname

    @staticmethod
    def total_teachers():
        return Teacher.objects.count() 

class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    Course_CHOICES = [
        ('class1','class1'),
        ('class2','class2'),
        ( 'class3','class3'),
        ( 'class4' ,'class4'),
        ( 'class5','class5'),
        ( 'class6','class6'),
        ( 'class7','class7'),
        ( 'class8','class8'),
        ( 'class9','class9'),
        ( 'class10', 'class10'),
       
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Firstname = models.CharField(max_length = 120)
    Lastname = models.CharField(max_length = 120)
    Email = models.EmailField(max_length = 50, unique = True)
    Gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    Password = models.CharField(max_length = 20)
    Profile = models.ImageField(upload_to = '')
    Co = models.CharField(max_length=10, choices=Course_CHOICES)
    Session = models.DateTimeField(auto_now_add = True)
    @classmethod
    def total_students(cls):
        return cls.objects.count()
    # Other fields for your Student model

    def total_present_days(self):
        return self.attendance_set.filter(is_present=True).count()
    def __str__(self):
        return f"{self.Firstname} - {self.Co}"

    
        
class Userdata(models.Model):
    Username=models.CharField(max_length=20)
    Email=models.EmailField(max_length=30)
    Password=models.CharField(max_length=10)
    def __str__(self):
        return self.Username

class Userdata1(models.Model):
    Username=models.CharField(max_length=20)
    Email=models.EmailField(max_length=30)
    Password=models.CharField(max_length=10)
    def __str__(self):
        return self.Username

class Course(models.Model):
    name = models.CharField(max_length=120)
    academic = models.PositiveIntegerField(default=1)
    # is_active = models.BooleanField(default=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    # description = models.TextField(blank=True, null=True)
    # instructor = models.CharField(max_length=255, blank=True, null=True)
    # start_date = models.DateField()
    # end_date = models.DateField()
    
    

    def __str__(self):
        return self.name
    

class Subject(models.Model):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    # credit = models.PositiveIntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Session(models.Model):
    name = models.CharField(max_length=120)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    subjects = models.ManyToManyField('Subject', related_name='sessions', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


#review
class StudentFeedback(models.Model):
    student = models.ForeignKey('finalapp.Student', on_delete=models.CASCADE)
    feedback_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.created_at}"

class TeacherFeedback(models.Model):
    teacher = models.ForeignKey('finalapp.Teacher', on_delete=models.CASCADE)
    feedback_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher} - {self.created_at}"

#leave
class StudentLeave(models.Model):
    student = models.ForeignKey('finalapp.Student', on_delete=models.CASCADE)
    reason = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_approved = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.start_date} to {self.end_date}"

class TeacherLeave(models.Model):
    teacher = models.ForeignKey('finalapp.Teacher', on_delete=models.CASCADE)
    reason = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_approved = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher} - {self.start_date} to {self.end_date}"

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    def _str_(self):
        return self.name


class StudentForm(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    GRADE_CHOICES = [
        ('1', 'class1'),
        ('2', 'class2'),
        ('3', 'class3'),
        ('4', 'class4'),
        ('5', 'class5'),
        ('6', 'class6'),
        ('7', 'class7'),
        ('8', 'class8'),
        ('9', 'class9'),
        ('10', 'class10'),
       
    
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    enter_dob = models.DateField() 
    parent_name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=15)
    enter_email = models.EmailField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES)
    address = models.TextField(max_length=200)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
class StudentAdmission(models.Model):
    student_form = models.ForeignKey(StudentForm, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_form.first_name} {self.student_form.last_name} Admission"

class TeacherJob(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]
    first_name    = models.CharField(max_length=100)
    last_name     = models.CharField(max_length=100)
    enter_email         = models.EmailField()
    phone_num  = models.CharField(max_length=15)
    resume        = models.FileField(upload_to='resumes/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Notice(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

    

class QuestionPaper(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='question_papers/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class AnswerSheet(models.Model):
    question_paper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='answer_sheets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

   
    


class Fee(models.Model):
    fee_id=models.CharField(max_length=20)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_fees')
    updated_at = models.DateTimeField(auto_now_add=True)
    def total(self):
        return self.amount


class Payment(models.Model):
    fee=models.ForeignKey(Fee,on_delete=models.PROTECT)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    def __str__(self):
        return self.fee.class_name
    


class Attendance(models.Model):
    student= models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)
    present_status = models.CharField(max_length=10)

    
    

    def __str__(self):
        return f"{self.student.Firstname} - {self.date} - {'Present' if self.is_present else 'Absent'}"
    
    
    
class Result(models.Model):
    class_name = models.CharField(max_length=100)
    result_file = models.FileField(upload_to='result_files/')


class AttendanceForm(forms.Form):
    def __init__(self, course, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)
        students = Student.objects.filter(Co=course)
        for student in students:
            self.fields['student_{}'.format(student.id)] = forms.BooleanField(
                label='{} {}'.format(student.Firstname, student.Lastname),
                required=False
            )

# models.py
from django.db import models

class ExcelFile(models.Model):
    file = models.FileField(upload_to='excel_files/')

    def __str__(self):
        return self.file.name
