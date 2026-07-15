import random
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import update_last_login
from django.core.cache import cache
from django.core.mail import send_mail
from .models import User
from .forms import (
    RegisterForm,
    LoginForm,
    ForgotPasswordForm,
    VerifyOTPForm,
    ResetPasswordForm,
    
)

from courses.models import Course
from departments.models import Department
from attendences.models import Attendance
from reports.models import Report

from students.forms import StudentForm   
from students.models import Student
from teachers.models import Teacher
from timetable.models import Timetable
from exams.models import Exam
from placement.models import Placement
from placement.models import Company
from teachers.forms import TeacherForm
from departments.forms import DepartmentForm
from courses.forms import CourseForm
from timetable.forms import TimetableForm
from attendences.forms import AttendanceForm
from exams.forms import ExamForm
from marks.models import Marks
from marks.forms import MarksForm
from placement.forms import CompanyForm
from placement.forms import PlacementForm
from reports.forms import ReportForm
from event.models import Event
from event.forms import EventForm



def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            messages.success(request, "Registration Successful")

    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {
        "form": form,
    })



def login_view(request):

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            update_last_login(None, user)

            

            if user.role == "ADMIN":
                return redirect("admin_dashboard")

            elif user.role == "TEACHER":
                return redirect("teacher_dashboard")

            elif user.role == "STUDENT":
                return redirect("student_dashboard")

            else:
                return redirect("login")

    else:
        form = LoginForm()

    return render(
        request,
        "accounts/login.html",
        {"form": form},
    )


@login_required
def admin_dashboard(request):

    section = request.GET.get("section", "dashboard")

    context = {
        "section": section,

        "students_count": User.objects.filter(role="STUDENT").count(),
        "teacher_count": User.objects.filter(role="TEACHER").count(),
        "course_count": Course.objects.count(),
        "department_count": Department.objects.count(),
        "attendance_count": Attendance.objects.count(),
        "report_count": Report.objects.count(),
        "company_count": Company.objects.count(),
        "placement_count": Placement.objects.count(),
    }

    context["recent_users"] = User.objects.order_by("-id")[:5]

    if section == "students":
        context["students"] = Student.objects.select_related(
            "user",
            "department",
            "course"
        )

    elif section == "teachers":
        context["teachers"] = Teacher.objects.select_related(
            "user",
            "department"
        )

    elif section == "departments":
        context["departments"] = Department.objects.all()

    elif section == "courses":
        context["courses"] = Course.objects.select_related(
            "department"
        )

    elif section == "timetable":

        context["timetables"] = Timetable.objects.select_related(
            "course",
            "teacher__user"
        ) 


    elif section == "attendance":
        context["attendance"] = Attendance.objects.select_related(
            "student",
            "student__user"
        ).order_by("-date")   


    elif section == "exams":
        context["exams"] = Exam.objects.select_related(
            "course"
        ).order_by("-exam_date")    


    elif section == "placements":

        context["placements"] = Placement.objects.select_related(
            "student",
            "student__user",
            "company"
        ).order_by("-placement_date")   


    elif section == "company":
        context["companies"] = Company.objects.all().order_by("name")

    elif section == "reports":
        context["reports"] = Report.objects.select_related(
            "generated_by"
        ).order_by("-generated_on")


    elif section == "users":
        context["users"] = User.objects.all().order_by("name")   


    elif section == "events":

        context["events"] = Event.objects.select_related(
            "organized_by"
    ).order_by("-event_date")
        

    elif section == "event_create":

        if request.method == "POST":

            form = EventForm(request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, "Event created successfully.")
                return redirect("/admin_dashboard/?section=events")

        else:
            form = EventForm()

        context["form"] = form



    elif section == "student_detail":

        student_id = request.GET.get("id")


        context["student"] = Student.objects.select_related(

            "user",
            "department",
            "course"
        ).get(id=student_id)  

    elif section == "student_update":

        student = Student.objects.select_related(
            "user",
            "department",
            "course"
        ).get(id=request.GET.get("id"))


        if request.method == "POST":

            form = StudentForm(request.POST, instance=student)


            if form.is_valid():

                form.save()

                return redirect("/admin_dashboard/?section=students")

        else:

            form = StudentForm(instance=student)

        context["form"] = form
        context["student"] = student 


    elif section == "teacher_create":

        if request.method == "POST":

            form = TeacherForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect("/admin_dashboard/?section=teachers")

        else:
            form = TeacherForm()

        context["form"] = form     


    elif section == "teacher_detail":


        teacher = Teacher.objects.select_related(
            "user",
            "department"
        ).get(id=request.GET.get("id"))

        context["teacher"] = teacher  


    elif section == "department_create":

        if request.method == "POST":

            form = DepartmentForm(request.POST)

            if form.is_valid():

                form.save()

                return redirect("/admin_dashboard/?section=departments")

        else:

            form = DepartmentForm()

        context["form"] = form    



    elif section == "department_detail":

        department = Department.objects.get(

            id=request.GET.get("id")
        )


        context["department"] = department 



    elif section == "department_update":

        department = Department.objects.get(

            id=request.GET.get("id")
        )


        if request.method == "POST":


            form = DepartmentForm(

                request.POST,
                instance=department
            )


            if form.is_valid():

                form.save()

                return redirect("/admin_dashboard/?section=departments")

        else:

            form = DepartmentForm(instance=department)

        context["form"] = form
        context["department"] = department



    elif section == "course_create":

        if request.method == "POST":

            form = CourseForm(request.POST)

            if form.is_valid():

                form.save()

                return redirect("/admin_dashboard/?section=courses")

        else:

            form = CourseForm()

        context["form"] = form      


    elif section == "course_detail":

        course = Course.objects.select_related(
            "department"
        ).get(id=request.GET.get("id"))

        context["course"] = course


    elif section == "course_update":

        course = Course.objects.select_related(

            "department"
        ).get(id=request.GET.get("id"))

        if request.method == "POST":

            form = CourseForm(
                request.POST,
                instance=course
            )

            if form.is_valid():
                form.save()
                return redirect("/admin_dashboard/?section=courses")

        else:
            form = CourseForm(instance=course)

        context["form"] = form
        context["course"] = course       

    
           


    elif section == "teacher_update":

        teacher = Teacher.objects.select_related(
            "user",
            "department"
        ).get(id=request.GET.get("id"))


        if request.method == "POST":


            form = TeacherForm(request.POST, instance=teacher)


            if form.is_valid():

                form.save()

                return redirect("/admin_dashboard/?section=teachers")

        else:

            form = TeacherForm(instance=teacher)

        context["form"] = form
        context["teacher"] = teacher 

    elif section == "timetable_create":

        if request.method == "POST":

            form = TimetableForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect("/admin_dashboard/?section=timetable")

        else:
            form = TimetableForm()

        context["form"] = form



    elif section == "timetable_detail":

        timetable = Timetable.objects.select_related(
            "course",
            "teacher__user"
        ).get(id=request.GET.get("id"))

        context["timetable"] = timetable 


    elif section == "timetable_update":

        timetable = Timetable.objects.select_related(
            "course",
            "teacher"
        ).get(id=request.GET.get("id"))

        if request.method == "POST":

            form = TimetableForm(
                request.POST,
                instance=timetable
            )

            if form.is_valid():
                form.save()
                return redirect("/admin_dashboard/?section=timetable")

        else:
            form = TimetableForm(instance=timetable)

        context["form"] = form
        context["timetable"] = timetable 


    elif section == "attendance_create":

        if request.method == "POST":

            form = AttendanceForm(request.POST)

            if form.is_valid():

                form.save()

                return redirect("/admin_dashboard/?section=attendance")

        else:

            form = AttendanceForm()

        context["form"] = form    




    elif section == "attendance_detail":

        print(request.GET)

        attendance = Attendance.objects.select_related(
            "student",
            "student__user"

        ).get(id=request.GET.get("id"))

        context["attendance"] = attendance


    elif section == "attendance_update":

        attendance = Attendance.objects.select_related(
            "student",
            "student__user"
        ).get(id=request.GET.get("id"))

        if request.method == "POST":

            form = AttendanceForm(
                request.POST,
                instance=attendance
            )

            if form.is_valid():
                form.save()
                return redirect("/admin_dashboard/?section=attendance")

        else:
            form = AttendanceForm(instance=attendance)

        context["form"] = form
        context["attendance"] = attendance



      



    elif section == "exam_create":


        if request.method == "POST":


            form = ExamForm(request.POST)


            if form.is_valid():


                form.save()


                return redirect("/admin_dashboard/?section=exams")

        else:

            form = ExamForm()


            context["form"] = form  


    elif section == "results":
            

            context["marks"] = Marks.objects.select_related(
                "student",
                "student__user",
                "course"
            ).order_by("-id")  


    elif section == "result_create":

        if request.method == "POST":

            form = MarksForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect("/admin_dashboard/?section=results")
            else:

                print(form.errors)  

        else:
            form = MarksForm()

        context["form"] = form  


    elif section == "company_create":

        if request.method == "POST":

            form = CompanyForm(request.POST)

            if form.is_valid():

                form.save()

                return redirect("/admin_dashboard/?section=company")

        else:

            form = CompanyForm()

        context["form"] = form  


    elif section == "placement_create":

        if request.method == "POST":

            form = PlacementForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect("/admin_dashboard/?section=placements")

        else:
            form = PlacementForm()

        context["form"] = form


    elif section == "report_create":

        if request.method == "POST":

            form = ReportForm(request.POST, request.FILES)

            if form.is_valid():
                form.save()
                return redirect("/admin_dashboard/?section=reports")

        else:

            form = ReportForm()

        context["form"] = form


    elif section == "exam_detail":

        exam = Exam.objects.select_related(
            "course"
        ).get(id=request.GET.get("id"))

        context["exam"] = exam  



    elif section == "exam_update":

        exam = Exam.objects.select_related(
            "course"
        ).get(id=request.GET.get("id"))


        if request.method == "POST":

            form = ExamForm(
                request.POST,
                instance=exam
            )

            if form.is_valid():
                form.save()
                return redirect("/admin_dashboard/?section=exams")

        else:
            form = ExamForm(instance=exam)

        context["form"] = form
        context["exam"] = exam



    elif section == "result_detail":

        mark = Marks.objects.select_related(
            "student",
            "student__user",
            "course"
        ).get(id=request.GET.get("id"))

        context["mark"] = mark




    elif section == "result_update":

        mark = Marks.objects.select_related(
            "student",
            "course"
        ).get(id=request.GET.get("id"))

        if request.method == "POST":

            form = MarksForm(
                request.POST,
                instance=mark
            )

            if form.is_valid():
                form.save()
                return redirect("/admin_dashboard/?section=results")

        else:
            form = MarksForm(instance=mark)

        context["form"] = form
        context["mark"] = mark 


    elif section == "placement_detail":

        placement = Placement.objects.select_related(
            "student",
            "student__user",
            "company"
        ).get(id=request.GET.get("id"))

        context["placement"] = placement 



    elif section == "placement_update":

        placement = Placement.objects.select_related(
            "student",
            "company"
        ).get(id=request.GET.get("id"))

        if request.method == "POST":

            form = PlacementForm(
                request.POST,
                instance=placement
            )

            if form.is_valid():
                form.save()
                return redirect("/admin_dashboard/?section=placements")

        else:
            form = PlacementForm(instance=placement)

        context["form"] = form
        context["placement"] = placement



    elif section == "company_detail":

        company = Company.objects.get(
            id=request.GET.get("id")
        )

        context["company"] = company


    elif section == "company_update":

        company = Company.objects.get(
            id=request.GET.get("id")
        )

        if request.method == "POST":

            form = CompanyForm(
                request.POST,
                instance=company
            )

            if form.is_valid():
                form.save()
                return redirect("/admin_dashboard/?section=company")

        else:

            form = CompanyForm(instance=company)

        context["form"] = form
        context["company"] = company



    elif section == "report_detail":

        report = Report.objects.select_related(
            "generated_by"
        ).get(id=request.GET.get("id"))

        context["report"] = report


    elif section == "report_update":

        report = Report.objects.select_related(
            "generated_by"
        ).get(id=request.GET.get("id"))

        if request.method == "POST":

            form = ReportForm(
                request.POST,
                request.FILES,
                instance=report
            )

            if form.is_valid():
                form.save()
                return redirect("/admin_dashboard/?section=reports")

        else:

            form = ReportForm(instance=report)

        context["form"] = form
        context["report"] = report



    elif section == "student_delete":

        student = get_object_or_404(
            Student.objects.select_related("user"),
            id=request.GET.get("id")
        )

        student.user.delete()

        return redirect("/admin_dashboard/?section=students")  




    elif section == "event_detail":

        event = Event.objects.select_related(
            "organized_by"
        ).get(id=request.GET.get("id"))

        context["event"] = event



    elif section == "event_update":

        event = Event.objects.select_related(
            "organized_by"
        ).get(id=request.GET.get("id"))

        if request.method == "POST":

            form = EventForm(
                request.POST,
                instance=event
            )

            if form.is_valid():
                form.save()
                return redirect("/admin_dashboard/?section=events")

        else:
            form = EventForm(instance=event)

        context["form"] = form
        context["event"] = event                                                               
                               


    elif section == "student_create":


        if request.method == "POST":

            form = StudentForm(request.POST)


            if form.is_valid():

                form.save()

                return redirect("/admin_dashboard/?section=students")

        else:

            form = StudentForm()


            context["form"] = form


      
    return render(request, "accounts/admin_dashboard.html", context)






@login_required
def logout_view(request):

    logout(request)

    messages.success(request, "Logout Successful")

    return redirect("login")


def forgot_password(request):

    if request.method == "POST":

        form = ForgotPasswordForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]

            try:
                User.objects.get(email=email)

            except User.DoesNotExist:

                messages.error(request, "User not found")

                return redirect("forgot-password")

            otp = str(random.randint(100000, 999999))

            cache.set(email, otp, timeout=300)

            send_mail(
                subject="Password Reset OTP",
                message=f"Your OTP is {otp}",
                from_email=None,
                recipient_list=[email],
                fail_silently=False,
            )


            return redirect("verify-otp")

    else:

        form = ForgotPasswordForm()

    return render(
        request,
        "accounts/forgot_password.html",
        {"form": form},
    )


def verify_otp(request):

    if request.method == "POST":

        form = VerifyOTPForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]

            otp = form.cleaned_data["otp"]

            saved_otp = cache.get(email)

            if saved_otp != otp:

                messages.error(request, "Invalid OTP")

                return redirect("verify-otp")

            messages.success(request, "OTP Verified Successfully")

            return redirect("reset-password")

    else:

        form = VerifyOTPForm()

    return render(
        request,
        "accounts/verify_otp.html",
        {"form": form},
    )


def reset_password(request):

    if request.method == "POST":

        form = ResetPasswordForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]

            otp = form.cleaned_data["otp"]

            saved_otp = cache.get(email)

            if saved_otp != otp:

                messages.error(request, "Invalid OTP")

                return redirect("reset-password")

            user = User.objects.get(email=email)

            user.set_password(
                form.cleaned_data["password"]
            )

            user.save()

            cache.delete(email)

            messages.success(
                request,
                "Password Reset Successfully"
            )

            return redirect("login")

    else:

        form = ResetPasswordForm()

    return render(
        request,
        "accounts/reset_password.html",
        {"form": form},
    )




def logout_view(request):
    logout(request)
    return redirect("login")