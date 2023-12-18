from finalapp.models import Student,Teacher

def get_student(request):
    return Student.objects.all()
def get_teacher(request):
    return Teacher.objects.all()
def get_student_by_id(student_id):
    try:
        # Try to get the student by ID
        student = Student.objects.get(id=student_id)
        return student
    except Student.DoesNotExist:
        # Handle the case where the student is not found
        return None
