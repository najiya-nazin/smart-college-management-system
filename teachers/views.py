from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from .models import Teacher
from accounts.models import Role
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from courses.models import Course
from timetable.models import Timetable
from courses.models import Course
from courses.forms import CourseForm
from students.models import Student
from attendences.models import Attendance
from attendences.forms import AttendanceForm
from exams.models import Exam
from marks.models import Marks
from reports.models import Report
from reports.forms import ReportForm
from django.utils import timezone
from .forms import TeacherUpdateForm, TeacherCreateForm,TeacherProfileForm
from teachers.models import Teacher
from departments.models import Department
from django.contrib import messages



from django.db.models import Count
from django.db.models.functions import ExtractWeekDay



# User = get_user_model()

# # Create Teacher
# def add_teacher(request):
#     form = TeacherForm()

#     users = User.objects.filter(role="TEACHER")
#     print(users)

#     if request.method == "POST":
#         form = TeacherForm(request.POST)

#         if form.is_valid():
#             form.save()
#             return redirect("teacher_list")

#     return render(request, "teacher/add_teacher.html", {
#         "form": form,
#         "users": users,
#     })

# # List Teachers
# def teacher_list(request):
#     teachers = Teacher.objects.all()

#     return render(request, "teacher/teacher_list.html", {
#         "teachers": teachers
#     })



def add_teacher(request):

    if request.method == "POST":
        form = TeacherCreateForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("teacher_list")

    else:
        form = TeacherCreateForm()

    return render(request, "teacher/add_teacher.html", {
        "form": form,
    })




def teacher_list(request):

    teachers = Teacher.objects.select_related(
        "user",
        "department"
    )

    search = request.GET.get("search")
    department = request.GET.get("department")

    if search:
        teachers = teachers.filter(
            user__name__icontains=search
        )

    if department:
        teachers = teachers.filter(
            department_id=department
        )

    departments = Department.objects.all()

    context = {
        "teachers": teachers,
        "departments": departments,
        "search": search,
        "selected_department": department,
    }

    return render(
        request,
        "teacher/teacher_list.html",
        context,
    )


# Teacher Detail
def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    return render(request, "teacher/teacher_detail.html", {
        "teacher": teacher
    })


# Update Teacher


def edit_teacher(request, pk):

    teacher = get_object_or_404(
        Teacher,
        pk=pk
    )

    if request.method == "POST":

        form = TeacherUpdateForm(
            request.POST,
            instance=teacher
        )

        if form.is_valid():
            form.save()
            return redirect("teacher_list")

    else:
        form = TeacherUpdateForm(
            instance=teacher
        )

    return render(
        request,
        "teacher/edit_teacher.html",
        {
            "form": form,
            "teacher": teacher,
        }
    )


def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    if request.method == "POST":
        teacher.delete()
        return redirect("teacher_list")

    return render(request, "teacher/delete_teacher.html", {
        "teacher": teacher
    })






# def teacher_dashboard(request):
#     section = request.GET.get("section", "dashboard")

#     return render(request, "teacher/teacher_dashboard.html", {
#         "section": section,
#     })



@login_required
def teacher_dashboard(request):
    teacher = get_object_or_404(
        Teacher,
        user=request.user
    )

    section = request.GET.get("section", "dashboard")

    my_courses = Timetable.objects.filter(
    teacher=teacher
).select_related("course")

    timetables = Timetable.objects.filter(
    teacher=teacher
).select_related("course")

    students = Student.objects.filter(
    department_id=teacher.department_id
).select_related(
    "user",
    "department"
)
    
    attendance = Attendance.objects.select_related(
    "student",
    "student__user",
    "student__department"
).all().order_by("-date")

    exams = Exam.objects.filter(
    course__in=my_courses.values_list("course", flat=True)
).select_related("course")

    marks = Marks.objects.filter(
    course__in=my_courses.values_list("course", flat=True)
).select_related(
    "student",
    "student__user",
    "course"
)

    reports = Report.objects.filter(
    generated_by=request.user
).order_by("-generated_on")
    

    students = Student.objects.select_related(
    "user",
    "department"
).all()

    

    courses_count = my_courses.values("course").distinct().count()

    today_classes_count = Timetable.objects.filter(
    teacher=teacher,
    day=timezone.now().strftime("%A")
).count()



    exam_count = exams.count()

    results_count = marks.count()

    recent_students = Student.objects.filter(
        course__in=my_courses.values_list("course", flat=True)

).select_related("user").order_by("-id")[:5]

    attendance_chart = [
            {"day": "Mon", "attendance": 42},
            {"day": "Tue", "attendance": 35},
            {"day": "Wed", "attendance": 48},
            {"day": "Thu", "attendance": 40},
            {"day": "Fri", "attendance": 45},
        ]




    form = TeacherCreateForm(instance=teacher)
    attendance_form = AttendanceForm()
    report_form = ReportForm()

    if section == "edit_profile":

        if request.method == "POST":
            form = TeacherProfileForm(request.POST, instance=teacher)

            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect(f"{reverse('teacher_dashboard')}?section=profile")
            else:
                print(form.errors)   

        

    elif section == "attendance" and request.method == "POST":

        attendance_form = AttendanceForm(request.POST)


        print(attendance.count())
        print(attendance)

        if attendance_form.is_valid():
            attendance_form.save()
            messages.success(request, "Attendance added successfully.")
            return redirect(
            f"{reverse('teacher_dashboard')}?section=attendance"
            )
        else:
            print(attendance_form.errors)



    elif request.method == "POST" and section == "reports":

        report_form = ReportForm(
            request.POST,
            request.FILES
        )


        if report_form.is_valid():


            report = report_form.save(commit=False)
            report.generated_by = request.user
            report.save()


            return redirect(
                f"{reverse('teacher_dashboard')}?section=reports"
            )

    else:
        form = TeacherCreateForm(instance=teacher)







    context = {
        "teacher": teacher,
        "form": form,
        "attendance_form": attendance_form,
        "section": section,
        "my_courses":my_courses,
        "timetables":timetables,
        "students":students,
        "attendance_list":attendance,
        "exams": exams,
        "marks": marks,
        "reports":reports,
        "report_form":report_form,
        "students": students,

       
        "courses_count":courses_count,
        "exam_count":exam_count,
        "today_classes_count":today_classes_count,
        "exam_count":exam_count,
        "results_count":results_count,
        "recent_students":recent_students,

        "attendance_chart": attendance_chart,


    }

    return render(
        request,
        "teacher/teacher_dashboard.html",
        context,
    )



def logout_view(request):
    logout(request)
    return redirect("login")





