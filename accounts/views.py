import random
from datetime import date
from django.db.models import Sum
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import update_last_login
from django.core.cache import cache
from django.core.mail import send_mail
from .models import User
from .forms import (RegisterForm, LoginForm, ForgotPasswordForm, VerifyOTPForm, ResetPasswordForm)
from courses.models import Course
from courses.forms import CourseForm
from departments.models import Department
from departments.forms import DepartmentForm
from attendences.models import Attendance
from attendences.forms import AttendanceForm
from attendences.models import AttendanceStatus
from reports.models import Report
from reports.forms import ReportForm
from students.forms import StudentForm, StudentProfileForm, UserProfileForm
from students.models import Student
from teachers.models import Teacher
from teachers.forms import TeacherForm
from timetable.models import Timetable
from timetable.forms import TimetableForm
from exams.models import Exam
from exams.forms import ExamForm
from placement.models import Placement
from placement.forms import PlacementForm
from placement.models import Company
from placement.forms import CompanyForm
from marks.models import Marks
from marks.forms import MarksForm
from event.models import Event
from fees.models import Fee, PaymentStatus
from library.models import Library
from library.models import LibraryStatus
from collections import OrderedDict


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration Successful")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            update_last_login(None, user)
            messages.success(request, "Login Successful")

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
    return render(request, "accounts/login.html", {"form": form})


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
    }

    if section == "students":
        context["students"] = Student.objects.select_related(
                  "user",
                  "department"
                  ).prefetch_related(
                   "courses"
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

    elif section == "student_detail":
        student_id = request.GET.get("id")
        context["student"] = Student.objects.select_related(
            "user",
            "department"
            ).prefetch_related(
            "course"
        ).get(id=student_id)  

    elif section == "student_update":
        student = Student.objects.select_related(
            "user",
            "department"
            ).prefetch_related(
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
        department = Department.objects.get(id=request.GET.get("id"))
        context["department"] = department 

    elif section == "department_update":
        department = Department.objects.get(id=request.GET.get("id"))

        if request.method == "POST":
            form = DepartmentForm(request.POST, instance=department)

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
            form = CourseForm(request.POST, instance=course)

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
            form = TimetableForm(request.POST, instance=timetable)

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
            form = AttendanceForm(request.POST, instance=attendance)
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
def student_dashboard(request):

    if request.user.role != "STUDENT":
        return HttpResponseForbidden(
            "You are not authorized to access this page."
        )

    student = Student.objects.select_related(
        "user",
        "department"
        ).prefetch_related(
        "course"
    ).get(
        user=request.user
    )

    section = request.GET.get(
        "section",
        "dashboard"
    )

    context = {
        "student": student,
        "section": section,
    }

    if section == "dashboard":

        attendance = Attendance.objects.filter(
            student=student
        )
        highest_mark = Marks.objects.filter(
            student=student
        ).order_by("-marks_obtained").first()

        context.update({

            "attendance_count": attendance.count(),

            "highest_mark": highest_mark,

            "library_count": Library.objects.filter(
                student=student,
                status="Issued"
            ).count(),

            "pending_fees": Fee.objects.filter(
                student=student
            ),

            "upcoming_exams": Exam.objects.filter(course__in=student.course.all()).order_by("exam_date")[:5],

            "events": Event.objects.order_by("-event_date")[:5],

            "timetables": Timetable.objects.filter(course__in=student.course.all())[:5],

            "placements": Placement.objects.filter(
                student=student
            ),

            "marks": Marks.objects.filter(
                student=student
            )[:5],
        })

    elif section == "profile":

        if request.method == "POST":
            student_form = StudentProfileForm(request.POST, instance=student)
            user_form = UserProfileForm(request.POST, instance=request.user)

            if student_form.is_valid() and user_form.is_valid():
                student_form.save()
                user_form.save()
                return redirect("/student_dashboard/?section=profile")

        else:
            student_form = StudentProfileForm(instance=student)
            user_form = UserProfileForm(instance=request.user)

        context.update({
            "student": student,
            "student_form": student_form,
            "user_form": user_form,
        })

    elif section == "course":
        context["courses"] = student.course.all()

    elif section == "attendance":

        attendance = Attendance.objects.filter(
            student=student
        ).order_by("-date")

        present_count = attendance.filter(
            status=AttendanceStatus.PRESENT
        ).count()

        absent_count = attendance.filter(
            status=AttendanceStatus.ABSENT
        ).count()

        late_count = attendance.filter(
            status=AttendanceStatus.LATE
        ).count()

        total = attendance.count()
        attendance_percentage = 0
        if total > 0:
            attendance_percentage = ((present_count + late_count) / total) * 100

        context.update({
            "attendance": attendance,
            "present_count": present_count,
            "absent_count": absent_count,
            "late_count": late_count,
            "attendance_percentage": attendance_percentage,
        })

    elif section == "marks":
        marks = Marks.objects.filter(student=student)
        highest_mark = marks.order_by("-marks_obtained").first()
        average_percentage = 0

        if marks.exists():
            percentages = [
                (mark.marks_obtained / mark.max_marks) * 100
                for mark in marks
            ]
            average_percentage = sum(percentages) / len(percentages)

        if average_percentage >= 90:
            overall_grade = "A+"
        elif average_percentage >= 80:
            overall_grade = "A"
        elif average_percentage >= 70:
            overall_grade = "B+"
        elif average_percentage >= 60:
            overall_grade = "B"
        elif average_percentage >= 50:
            overall_grade = "C"
        else:
            overall_grade = "F"

        context.update({
            "marks": marks,
            "highest_mark": highest_mark,
            "average_percentage": average_percentage,
            "overall_grade": overall_grade,
        })

    elif section == "timetable":

        timetable_qs = (

            Timetable.objects.filter(course__in=student.course.all())

            .select_related("course", "teacher__user")

            .order_by("start_time", "day")

        )

        timetable = OrderedDict()

        for item in timetable_qs:

            slot = (

                item.start_time.strftime("%I:%M %p"),

                item.end_time.strftime("%I:%M %p")

            )

            if slot not in timetable:
                timetable[slot] = {

                    "Monday": None,

                    "Tuesday": None,

                    "Wednesday": None,

                    "Thursday": None,

                    "Friday": None,

                }

            timetable[slot][item.day] = item

        context["timetable"] = timetable

    elif section == "library":

        library = Library.objects.select_related(
            "book"
        ).filter(student=student)

        issued_books = library.filter(status=LibraryStatus.ISSUED).count()

        returned_books = library.filter(status=LibraryStatus.RETURNED).count()

        overdue_books = library.filter(status=LibraryStatus.ISSUED, due_date__lt=date.today()).count()

        total_fine = library.aggregate(total=Sum("fine"))["total"] or 0

        context.update({
            "library": library,
            "issued_books": issued_books,
            "returned_books": returned_books,
            "overdue_books": overdue_books,
            "total_fine": total_fine,
        })

    elif section == "fees":
        fees = Fee.objects.filter(
            student=student
        ).order_by(
            "-semester",
            "fee_type"
        )

        total_fee = 0
        total_paid = 0
        total_balance = 0

        for fee in fees:
            fee.balance = fee.amount - fee.paid_amount
            total_fee += fee.amount
            total_paid += fee.paid_amount
            total_balance += fee.balance

        payment_percentage = 0

        if total_fee > 0:
            payment_percentage = round((total_paid / total_fee) * 100, 1)

        context.update({
            "fees": fees,
            "total_fee": total_fee,
            "total_paid": total_paid,
            "total_balance": total_balance,
            "payment_percentage": payment_percentage,
            "total_payments": fees.count(),

        })

    elif section == "receipt":
        fee_id = request.GET.get("fee")
        fee = get_object_or_404(
            Fee,
            pk=fee_id,
            student=student
        )
        fee.balance = fee.amount - fee.paid_amount
        context["fee"] = fee

    elif section == "events":
        context["events"] = Event.objects.all()

    elif section == "exams":
        context["exams"] = Exam.objects.filter(course__in=student.course.all())

    elif section == "placement":
        context["placements"] = Placement.objects.filter(
            student=student
        )

    return render(request, "students/student_dashboard.html", context)


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
            messages.success(request, "OTP Sent Successfully")
            return redirect("verify-otp")

    else:
        form = ForgotPasswordForm()
    return render(request, "accounts/forgot_password.html",{"form": form},)


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
    return render(request, "accounts/verify_otp.html", {"form": form},)


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
            user.set_password(form.cleaned_data["password"])
            user.save()
            cache.delete(email)
            messages.success(request, "Password Reset Successfully")
            return redirect("login")

    else:
        form = ResetPasswordForm()
    return render(request, "accounts/reset_password.html", {"form": form},)
