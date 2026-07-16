import random
from django.shortcuts import render, redirect,get_object_or_404
from datetime import date
from django.db.models import Sum, Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import update_last_login
from django.core.cache import cache
from django.core.mail import send_mail
from django.urls import reverse

from .models import User, Role
from .forms import (LoginForm, ForgotPasswordForm, VerifyOTPForm, ResetPasswordForm)
from courses.models import Course
from courses.forms import CourseForm
from departments.models import Department
from departments.forms import DepartmentForm
from attendences.models import Attendance
from attendences.forms import AttendanceForm
from attendences.models import AttendanceStatus
from reports.models import Report
from reports.forms import ReportForm
from students.forms import StudentCreateForm, StudentProfileForm, UserProfileForm, StudentUpdateForm
from students.models import Student
from teachers.models import Teacher
from teachers.forms import TeacherCreateForm, TeacherUpdateForm
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
from placement.forms import CompanyForm
from placement.forms import PlacementForm
from reports.forms import ReportForm
from event.models import Event
from event.forms import EventForm
from event.models import Event
from fees.models import Fee, PaymentStatus
from library.models import Library
from library.models import LibraryStatus
from collections import OrderedDict
from django.db.models import Count
from django.utils import timezone
from django.db.models import Sum
from placement.models import PlacementStatus


# def register(request):
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             messages.success(request, "Registration Successful")
#     else:
#         form = RegisterForm()
#     return render(request, "accounts/register.html", {"form": form})

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

            elif user.role == Role.TEACHER:
                return redirect("teacher_dashboard")

            elif user.role == Role.STUDENT:
                return redirect("student_dashboard")

            return redirect("login")

    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


@login_required
def admin_dashboard(request):

    if request.user.role != Role.ADMIN:
        return HttpResponseForbidden(
            "You are not authorized to access this page."
        )

    section = request.GET.get(
        "section",
        "dashboard"
    )

    context = {
        "section": section,
    }

    if section == "dashboard":

        today = timezone.now().date()

        department_chart = (
            Department.objects
            .annotate(student_count=Count("students"))
            .order_by("name")
        )

        context.update({

            "students_count": Student.objects.count(),
            "teachers_count": Teacher.objects.count(),
            "departments_count": Department.objects.count(),
            "courses_count": Course.objects.count(),
            "attendance_count": Attendance.objects.count(),
            "placements_count": Placement.objects.count(),
            "companies_count": Company.objects.count(),
            "reports_count": Report.objects.count(),

            "department_chart": department_chart,

            "upcoming_events": Event.objects.filter(
                event_date__gte=today
            ).order_by(
                "event_date"
            )[:4],

            "recent_users": User.objects.order_by(
                "-created_at"
            )[:5],

            "today_attendance": Attendance.objects.filter(
                date=today
            ).count(),

            "today_events": Event.objects.filter(
                event_date=today
            ).count(),

            "today_exams": Exam.objects.filter(
                exam_date=today
            ).count(),

            "pending_fee_amount": Fee.objects.filter(
                status="Pending"
            ).aggregate(
                total=Sum("amount")
            )["total"] or 0,

            "recent_students": Student.objects.select_related(
                "user"
            ).order_by("-id")[:2],

            "recent_teachers": Teacher.objects.select_related(
                "user"
            ).order_by("-id")[:2],

            "recent_attendance": Attendance.objects.select_related(
                "student__user"
            ).order_by("-id")[:1],

            # "recent_placements": Placement.objects.select_related(
            #     "student__user",
            #     "company"
            # ).order_by("-id")[:1],

        })

    elif section == "users":

        context.update({

            "admins_count": User.objects.filter(
                role=Role.ADMIN
            ).count(),

            "users_count": User.objects.count(),

            "teachers_count": Teacher.objects.count(),

            "students_count": Student.objects.count(),

            "recent_students": Student.objects.select_related(
                "user",
                "department"
            ).order_by("-id")[:5],

            "recent_teachers": Teacher.objects.select_related(
                "user",
                "department"
            ).order_by("-id")[:5],
        })

    elif section == "students":

        students = Student.objects.select_related(
            "user",
            "department"
        ).prefetch_related(
            "course"
        )

        departments = Department.objects.all()

        search = request.GET.get("search", "")
        department = request.GET.get("department", "")

        if search:
            students = students.filter(
                Q(user__name__icontains=search) |
                Q(user__email__icontains=search) |
                Q(student_id__icontains=search)
            )

        if department:
            students = students.filter(
                department_id=department
            )

        context.update({
            "students": students,
            "departments": departments,
            "search": search,
            "selected_department": department,
        })

    elif section == "student_detail":

        student_id = request.GET.get("id")

        student = get_object_or_404(
            Student.objects.select_related(
                "user",
                "department"
            ).prefetch_related(
                "course"
            ),
            pk=student_id
        )

        context["student"] = student

    elif section == "student_update":

        student_id = request.GET.get("id")

        student = get_object_or_404(
            Student,
            pk=student_id
        )

        if request.method == "POST":

            form = StudentUpdateForm(
                request.POST,
                instance=student
            )

            if form.is_valid():
                form.save()

                return redirect(
                    reverse("admin_dashboard") + "?section=students"
                )

        else:

            form = StudentUpdateForm(
                instance=student
            )

        context.update({

            "form": form,

            "student": student,

        })

    elif section == "teachers":

        teachers = Teacher.objects.select_related(
            "user",
            "department"
        )

        departments = Department.objects.all()

        search = request.GET.get("search", "")
        department = request.GET.get("department", "")

        if search:
            teachers = teachers.filter(
                Q(user__name__icontains=search) |
                Q(user__email__icontains=search)
            )

        if department:
            teachers = teachers.filter(
                department_id=department
            )

        context.update({
            "teachers": teachers,
            "departments": departments,
            "search": search,
            "selected_department": department,
        })

    elif section == "student_create":

        if request.method == "POST":

            form = StudentCreateForm(request.POST)

            if form.is_valid():

                form.save()

                return redirect(
                    reverse("admin_dashboard") + "?section=students"
                )

            else:
                print(form.errors)

        else:

            form = StudentCreateForm()

        context.update({

            "form": form,

            "departments": Department.objects.all(),

            "courses": Course.objects.all(),

        })

    elif section == "teacher_create":

        if request.method == "POST":

            form = TeacherCreateForm(request.POST)

            if form.is_valid():
                user = User.objects.create_user(
                    email=form.cleaned_data["email"],
                    name=form.cleaned_data["name"],
                    password=form.cleaned_data["password"],
                    role=Role.TEACHER,
                    phone=form.cleaned_data["phone"],
                )

                Teacher.objects.create(
                    user=user,
                    department=form.cleaned_data["department"],
                    qualification=form.cleaned_data["qualification"],
                    experience=form.cleaned_data["experience"],
                    salary=form.cleaned_data["salary"],
                )

                return redirect("teacher_list")

        else:

            form = TeacherCreateForm()

        context["form"] = form

    elif section == "teacher_view":

        teacher = get_object_or_404(
            Teacher.objects.select_related(
                "user",
                "department"
            ),
            id=request.GET.get("id")
        )

        context["teacher"] = teacher

    elif section == "teacher_edit":

        teacher = get_object_or_404(
            Teacher,
            id=request.GET.get("id")
        )

        if request.method == "POST":

            form = TeacherUpdateForm(
                request.POST,
                instance=teacher
            )

            if form.is_valid():

                teacher.user.name = form.cleaned_data["name"]
                teacher.user.email = form.cleaned_data["email"]
                teacher.user.phone = form.cleaned_data["phone"]

                # if form.cleaned_data["password"]:
                #     teacher.user.set_password(
                #         form.cleaned_data["password"]
                #     )

                teacher.user.save()

                form.save()

                return redirect(
                    "/admin_dashboard/?section=teachers"
                )

        else:

            initial = {
                "name": teacher.user.name,
                "email": teacher.user.email,
                "phone": teacher.user.phone,
            }

            form = TeacherUpdateForm(
                instance=teacher,
                initial=initial
            )

        context["form"] = form

    elif section == "teacher_delete":

        teacher = get_object_or_404(
            Teacher,
            id=request.GET.get("id")
        )

        teacher.user.delete()

        return redirect(
            "/admin_dashboard/?section=teachers"
        )

    elif section == "departments":

        search = request.GET.get("search", "")

        departments = Department.objects.all()

        if search:
            departments = departments.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search)
            )

        context.update({
            "departments": departments.order_by("name"),
            "search": search,
        })

    elif section == "department_create":

        if request.method == "POST":
            form = DepartmentForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect(reverse("admin_dashboard") + "?section=departments")

        else:
            form = DepartmentForm()

        context["form"] = form

    elif section == "department_update":

        department = get_object_or_404(
            Department,
            pk=request.GET.get("id")
        )

        if request.method == "POST":
            form = DepartmentForm(
                request.POST,
                instance=department
            )

            if form.is_valid():
                form.save()
                return redirect(reverse("admin_dashboard") + "?section=departments")

        else:
            form = DepartmentForm(instance=department)

        context["form"] = form

    elif section == "department_detail":

        department = get_object_or_404(
            Department,
            pk=request.GET.get("id")
        )

        context["department"] = department

    elif section == "department_update":

        department = get_object_or_404(
            Department,
            pk=request.GET.get("id")
        )

        if request.method == "POST":
            form = DepartmentForm(
                request.POST,
                instance=department
            )

            if form.is_valid():
                form.save()
                return redirect(
                    reverse("admin_dashboard") + "?section=departments"
                )

        else:
            form = DepartmentForm(instance=department)

        context["form"] = form

    elif section == "courses":

        search = request.GET.get("search", "")
        selected_department = request.GET.get("department", "")

        courses = Course.objects.select_related("department").all()
        departments = Department.objects.all().order_by("name")

        # Search
        if search:
            courses = courses.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search)
            )

        # Department Filter
        if selected_department:
            courses = courses.filter(
                department_id=selected_department
            )

        context.update({
            "courses": courses.order_by("name"),
            "departments": departments,
            "search": search,
            "selected_department": selected_department,
        })

    elif section == "course_create":

        if request.method == "POST":

            form = CourseForm(request.POST)

            if form.is_valid():
                form.save()

                return redirect(
                    reverse("admin_dashboard") + "?section=courses"
                )

        else:
            form = CourseForm()

        context["form"] = form

    elif section == "course_update":

        course = get_object_or_404(
            Course,
            pk=request.GET.get("id")
        )

        if request.method == "POST":

            form = CourseForm(
                request.POST,
                instance=course
            )

            if form.is_valid():
                form.save()

                return redirect(
                    reverse("admin_dashboard") + "?section=courses"
                )

        else:

            form = CourseForm(instance=course)

        context["form"] = form

    elif section == "course_detail":

        course = get_object_or_404(
            Course.objects.select_related("department"),
            pk=request.GET.get("id")
        )

        context["course"] = course

    elif section == "timetables":

        search = request.GET.get("search", "")
        selected_department = request.GET.get("department", "")
        selected_day = request.GET.get("day", "")

        timetables = Timetable.objects.select_related(
            "course",
            "course__department",
            "teacher",
            "teacher__user"
        )

        if search:
            timetables = timetables.filter(
                Q(course__name__icontains=search) |
                Q(teacher__user__name__icontains=search) |
                Q(class_name__icontains=search) |
                Q(room_no__icontains=search)
            )

        if selected_department:
            timetables = timetables.filter(
                course__department_id=selected_department
            )

        if selected_day:
            timetables = timetables.filter(
                day=selected_day
            )

        context.update({
            "timetables": timetables.order_by("day", "start_time"),
            "departments": Department.objects.all().order_by("name"),
            "selected_department": selected_department,
            "selected_day": selected_day,
            "search": search,
            "days": [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ],
        })

    elif section == "timetable_create":

        if request.method == "POST":

            form = TimetableForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect(
                    reverse("admin_dashboard")
                    + "?section=timetables"
                )

        else:
            form = TimetableForm()

        context["form"] = form

    elif section == "timetable_update":

        timetable = get_object_or_404(
            Timetable,
            pk=request.GET.get("id")
        )

        if request.method == "POST":

            form = TimetableForm(
                request.POST,
                instance=timetable
            )

            if form.is_valid():
                form.save()

                return redirect(
                    reverse("admin_dashboard") +
                    "?section=timetables"
                )

        else:

            form = TimetableForm(
                instance=timetable
            )

        context.update({
            "form": form,
            "timetable": timetable,
        })

    elif section == "timetable_detail":

        timetable = get_object_or_404(
            Timetable.objects.select_related(
                "course",
                "course__department",
                "teacher",
                "teacher__user",
            ),
            pk=request.GET.get("id")
        )

        context["timetable"] = timetable

    elif section == "attendances":

        search = request.GET.get("search", "")
        selected_department = request.GET.get("department", "")
        selected_date = request.GET.get("date", "")

        attendances = Attendance.objects.select_related(
            "student",
            "student__user",
            "student__department"
        )

        # Search by Student Name or Student ID
        if search:
            attendances = attendances.filter(
                Q(student__user__name__icontains=search) |
                Q(student__student_id__icontains=search)
            )

        # Filter by Department
        if selected_department:
            attendances = attendances.filter(
                student__department_id=selected_department
            )

        # Filter by Date
        if selected_date:
            attendances = attendances.filter(
                date=selected_date
            )

        context.update({

            "attendances": attendances.order_by(
                "-date",
                "student__user__name"
            ),

            "departments": Department.objects.order_by("name"),

            "selected_department": selected_department,
            "selected_date": selected_date,
            "search": search,

        })

    # elif section == "attendance_create":
    #
    #     if request.method == "POST":
    #
    #         form = AttendanceForm(request.POST)
    #
    #         if form.is_valid():
    #             form.save()
    #
    #             return redirect(
    #                 reverse("admin_dashboard")
    #                 + "?section=attendances"
    #             )
    #
    #     else:
    #
    #         form = AttendanceForm()
    #
    #     context["form"] = form
    #
    # elif section == "attendance_update":
    #
    #     attendance = get_object_or_404(
    #         Attendance,
    #         pk=request.GET.get("id")
    #     )
    #
    #     if request.method == "POST":
    #
    #         form = AttendanceForm(
    #             request.POST,
    #             instance=attendance
    #         )
    #
    #         if form.is_valid():
    #             form.save()
    #
    #             return redirect(
    #                 reverse("admin_dashboard")
    #                 + "?section=attendances"
    #             )
    #
    #     else:
    #
    #         form = AttendanceForm(
    #             instance=attendance
    #         )
    #
    #     context.update({
    #         "form": form,
    #         "attendance": attendance,
    #     })

    elif section == "attendance_detail":

        attendance = get_object_or_404(
            Attendance.objects.select_related(
                "student",
                "student__user",
                "student__department",
            ),
            pk=request.GET.get("id")
        )

        context["attendance"] = attendance

    elif section == "exams":

        search = request.GET.get("search", "")
        selected_department = request.GET.get("department", "")
        selected_course = request.GET.get("course", "")
        selected_date = request.GET.get("date", "")

        exams = Exam.objects.select_related(
            "course",
            "course__department"
        )

        # Search by Exam Name or Course
        if search:
            exams = exams.filter(
                Q(name__icontains=search) |
                Q(course__name__icontains=search)
            )

        # Filter by Department
        if selected_department:
            exams = exams.filter(
                course__department_id=selected_department
            )

        # Filter by Course
        if selected_course:
            exams = exams.filter(
                course_id=selected_course
            )

        # Filter by Date
        if selected_date:
            exams = exams.filter(
                exam_date=selected_date
            )

        context.update({

            "exams": exams.order_by(
                "exam_date",
                "name"
            ),

            "departments": Department.objects.order_by("name"),

            "courses": Course.objects.select_related(
                "department"
            ).order_by("name"),

            "search": search,
            "selected_department": selected_department,
            "selected_course": selected_course,
            "selected_date": selected_date,

        })

    elif section == "exam_create":

        if request.method == "POST":

            form = ExamForm(request.POST)

            if form.is_valid():
                form.save()

                return redirect(
                    reverse("admin_dashboard")
                    + "?section=exams"
                )

        else:

            form = ExamForm()

        context["form"] = form

    elif section == "exam_update":

        exam = get_object_or_404(
            Exam,
            pk=request.GET.get("id")
        )

        if request.method == "POST":

            form = ExamForm(
                request.POST,
                instance=exam
            )

            if form.is_valid():
                form.save()

                return redirect(
                    reverse("admin_dashboard")
                    + "?section=exams"
                )

        else:

            form = ExamForm(
                instance=exam
            )

        context.update({
            "form": form,
            "exam": exam,
        })

    elif section == "exam_detail":

        exam = get_object_or_404(
            Exam.objects.select_related(
                "course",
                "course__department",
            ),
            pk=request.GET.get("id")
        )

        context["exam"] = exam

    elif section == "marks":

        search = request.GET.get("search", "")
        selected_department = request.GET.get("department", "")
        selected_course = request.GET.get("course", "")
        selected_grade = request.GET.get("grade", "")

        marks = Marks.objects.select_related(
            "student",
            "student__user",
            "student__department",
            "course",
        )

        # ---------------- Search ----------------

        if search:
            marks = marks.filter(
                Q(student__user__name__icontains=search) |
                Q(student__student_id__icontains=search)
            )

        # ---------------- Department Filter ----------------

        if selected_department:
            marks = marks.filter(
                student__department_id=selected_department
            )

        # ---------------- Course Filter ----------------

        if selected_course:
            marks = marks.filter(
                course_id=selected_course
            )

        # ---------------- Grade Filter ----------------

        if selected_grade:
            marks = marks.filter(
                grade=selected_grade
            )

        # ---------------- Percentage & Result ----------------

        marks_list = []

        for mark in marks.order_by(
                "student__user__name",
                "course__name"
        ):

            percentage = 0

            if mark.max_marks > 0:
                percentage = round(
                    (mark.marks_obtained / mark.max_marks) * 100,
                    1
                )

            mark.percentage = percentage

            mark.result = (
                "Pass"
                if percentage >= 40
                else "Fail"
            )

            marks_list.append(mark)

        context.update({

            "marks": marks_list,

            "departments": Department.objects.order_by(
                "name"
            ),

            "courses": Course.objects.select_related(
                "department"
            ).order_by(
                "name"
            ),

            "grades": [
                "A+",
                "A",
                "B+",
                "B",
                "C",
                "D",
                "F",
            ],

            "search": search,

            "selected_department": selected_department,

            "selected_course": selected_course,

            "selected_grade": selected_grade,

        })

    elif section == "marks_create":

        if request.method == "POST":

            form = MarksForm(request.POST)

            if form.is_valid():
                form.save()

                return redirect(
                    reverse("admin_dashboard")
                    + "?section=marks"
                )

        else:

            form = MarksForm()

        context["form"] = form

    elif section == "marks_update":

        marks = get_object_or_404(
            Marks,
            pk=request.GET.get("id")
        )

        if request.method == "POST":

            form = MarksForm(
                request.POST,
                instance=marks
            )

            if form.is_valid():
                form.save()

                return redirect(
                    reverse("admin_dashboard")
                    + "?section=marks"
                )

        else:

            form = MarksForm(
                instance=marks
            )

        context.update({

            "form": form,

            "marks": marks,

        })

    elif section == "marks_detail":

        marks = get_object_or_404(

            Marks.objects.select_related(
                "student",
                "student__user",
                "student__department",
                "course",
            ),

            pk=request.GET.get("id")
        )

        percentage = 0

        if marks.max_marks > 0:
            percentage = round(
                (marks.marks_obtained / marks.max_marks) * 100,
                1
            )

        marks.percentage = percentage

        marks.result = (
            "Pass"
            if percentage >= 40
            else "Fail"
        )

        context["marks"] = marks

    elif section == "marks_delete":

        marks = get_object_or_404(
            Marks,
            pk=request.GET.get("id")
        )

        marks.delete()

        return redirect(
            reverse("admin_dashboard")
            + "?section=marks"
        )

    elif section == "placements":

        search = request.GET.get("search", "")
        selected_department = request.GET.get("department", "")
        selected_company = request.GET.get("company", "")
        selected_status = request.GET.get("status", "")
        selected_date = request.GET.get("date", "")

        placements = Placement.objects.select_related(
            "student",
            "student__user",
            "student__department",
            "company",
        )

        # Search

        if search:
            placements = placements.filter(
                Q(student__user__name__icontains=search) |
                Q(student__student_id__icontains=search) |
                Q(company__name__icontains=search) |
                Q(job_role__icontains=search)
            )

        # Department Filter

        if selected_department:
            placements = placements.filter(
                student__department_id=selected_department
            )

        # Company Filter

        if selected_company:
            placements = placements.filter(
                company_id=selected_company
            )

        # Status Filter

        if selected_status:
            placements = placements.filter(
                status=selected_status
            )

        # Placement Date Filter

        if selected_date:
            placements = placements.filter(
                placement_date=selected_date
            )

        context.update({

            "placements": placements.order_by(
                "-placement_date",
                "student__user__name"
            ),

            "departments": Department.objects.order_by(
                "name"
            ),

            "companies": Company.objects.order_by(
                "name"
            ),

            "statuses": PlacementStatus.choices,

            "search": search,

            "selected_department": selected_department,

            "selected_company": selected_company,

            "selected_status": selected_status,

            "selected_date": selected_date,

        })

    elif section == "placement_create":

        if request.method == "POST":

            form = PlacementForm(request.POST)

            if form.is_valid():
                form.save()

                return redirect(
                    reverse("admin_dashboard")
                    + "?section=placements"
                )

        else:

            form = PlacementForm()

        context["form"] = form

    elif section == "placement_update":

        placement = get_object_or_404(
            Placement,
            pk=request.GET.get("id")
        )

        if request.method == "POST":

            form = PlacementForm(
                request.POST,
                instance=placement
            )

            if form.is_valid():
                form.save()

                return redirect(
                    reverse("admin_dashboard")
                    + "?section=placements"
                )

        else:

            form = PlacementForm(
                instance=placement
            )

        context.update({

            "form": form,

            "placement": placement,

        })

    elif section == "placement_detail":

        placement = get_object_or_404(

            Placement.objects.select_related(
                "student",
                "student__user",
                "student__department",
                "company",
            ),

            pk=request.GET.get("id")

        )

        context["placement"] = placement

    elif section == "placement_delete":

        placement = get_object_or_404(
            Placement,
            pk=request.GET.get("id")
        )

        placement.delete()

        return redirect(
            reverse("admin_dashboard")
            + "?section=placements"
        )

    elif section == "companies":

        search = request.GET.get("search", "")
        selected_location = request.GET.get("location", "")

        companies = Company.objects.all()

        # Search

        if search:
            companies = companies.filter(

                Q(name__icontains=search) |
                Q(location__icontains=search) |
                Q(email__icontains=search)

            )

        # Location Filter

        if selected_location:
            companies = companies.filter(
                location=selected_location
            )

        context.update({

            "companies": companies.order_by("name"),

            "locations": Company.objects.values_list(
                "location",
                flat=True
            ).distinct().order_by("location"),

            "search": search,

            "selected_location": selected_location,

        })


    elif section == "company_create":

        if request.method == "POST":

            form = CompanyForm(request.POST)

            if form.is_valid():
                form.save()

                return redirect(
                    reverse("admin_dashboard")
                    + "?section=companies"
                )

        else:

            form = CompanyForm()

        context["form"] = form


    elif section == "company_update":

        company = get_object_or_404(
            Company,
            pk=request.GET.get("id")
        )

        if request.method == "POST":

            form = CompanyForm(
                request.POST,
                instance=company
            )

            if form.is_valid():
                form.save()

                return redirect(
                    reverse("admin_dashboard")
                    + "?section=companies"
                )

        else:

            form = CompanyForm(
                instance=company
            )

        context.update({

            "form": form,

            "company": company,

        })


    elif section == "company_detail":

        company = get_object_or_404(
            Company,
            pk=request.GET.get("id")
        )

        context["company"] = company


    elif section == "company_delete":

        company = get_object_or_404(
            Company,
            pk=request.GET.get("id")
        )

        company.delete()

        return redirect(
            reverse("admin_dashboard")
            + "?section=companies"
        )

    elif section == "events":

        search = request.GET.get("search", "")
        department = request.GET.get("department", "")

        events = Event.objects.select_related(
            "organized_by"
        ).all()

        # Search

        if search:
            events = events.filter(

                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(organized_by__name__icontains=search)

            )

        # Department Filter

        if department:
            events = events.filter(
                organized_by_id=department
            )

        context.update({

            "events": events.order_by("event_date"),

            "departments": Department.objects.all(),

            "search": search,

            "selected_department": department,

        })


    elif section == "event_create":

        if request.method == "POST":

            form = EventForm(request.POST)

            if form.is_valid():
                form.save()

                messages.success(
                    request,
                    "Event created successfully."
                )

                return redirect(
                    reverse("admin_dashboard")
                    + "?section=events"
                )

        else:

            form = EventForm()

        context["form"] = form


    elif section == "event_update":

        event = get_object_or_404(
            Event,
            pk=request.GET.get("id")
        )

        if request.method == "POST":

            form = EventForm(
                request.POST,
                instance=event
            )

            if form.is_valid():
                form.save()

                messages.success(
                    request,
                    "Event updated successfully."
                )

                return redirect(
                    reverse("admin_dashboard")
                    + "?section=events"
                )

        else:

            form = EventForm(
                instance=event
            )

        context.update({

            "form": form,

            "event": event,

        })


    elif section == "event_detail":

        event = get_object_or_404(

            Event.objects.select_related(
                "organized_by"
            ),

            pk=request.GET.get("id")

        )

        context["event"] = event


    elif section == "event_delete":

        event = get_object_or_404(
            Event,
            pk=request.GET.get("id")
        )

        event.delete()

        messages.success(
            request,
            "Event deleted successfully."
        )

        return redirect(
            reverse("admin_dashboard")
            + "?section=events"
        )

    elif section == "reports":

        search = request.GET.get("search", "")
        report_type = request.GET.get("report_type", "")

        reports = Report.objects.select_related(
            "generated_by"
        ).all()

        if search:
            reports = reports.filter(

                Q(report_type__icontains=search) |
                Q(generated_by__name__icontains=search) |
                Q(generated_by__email__icontains=search)

            )

        if report_type:
            reports = reports.filter(
                report_type=report_type
            )

        report_types = Report.objects.values_list(
            "report_type",
            flat=True
        ).distinct()

        context.update({

            "reports": reports,
            "report_types": report_types,
            "selected_report_type": report_type,
            "search": search,

        })

    elif section == "report_detail":

        report = get_object_or_404(
            Report.objects.select_related(
                "generated_by"
            ),
            pk=request.GET.get("id")
        )

        context["report"] = report

    elif section == "report_delete":

        report = get_object_or_404(
            Report,
            pk=request.GET.get("id")
        )

        if request.method == "POST":
            report.delete()

            messages.success(
                request,
                "Report deleted successfully."
            )

            return redirect(
                f"{reverse('admin_dashboard')}?section=reports"
            )

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
    return render(request, "accounts/forgot_password.html", {"form": form})


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

    return render(
        request,
        "accounts/reset_password.html",
        {"form": form},
    )


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logout Successful")
    return redirect("login")


