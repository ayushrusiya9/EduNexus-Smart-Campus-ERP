from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignupForm, LoginForm, StudentProfileForm,DepartmentForm,TeacherProfileForm,EbookForm,StudentProfileFormTeacher,StudentForm
from .models import User, StudentProfile,TeacherProfile,Department,EBook
from django.db.models import Q
from django.core.mail import send_mail
# Landing Page 
def landing_page(request):
    return render(request, 'landing.html')

def about(request):
    return render(request,'about.html')

def why_choose_us(request):
    return render(request,'whychooseus.html')

def contact(request):
    return render(request,'contact.html')

# ---------------- Sign Up ----------------
def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('Password')
            confirm_password = form.cleaned_data.get('Confirm_password')

            if password != confirm_password:
                form.add_error('Confirm_password', "Passwords do not match")
                return render(request, "signup_login.html", {"form": form})

            # Save new user
            form.save()
            return redirect('log_in')

        # agar form invalid hai
        return render(request, "signup_login.html", {"form": form})

    form = SignupForm()
    return render(request, "signup_login.html", {"form": form})


# ---------------- Log In ----------------
def log_in(request):
    adminemail="admin@gmail.com"
    adminpass = 'admin'
    login_form = LoginForm()
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        
        if login_form.is_valid():
            email = login_form.cleaned_data.get('Email')
            password = login_form.cleaned_data.get('Password')

            if email == adminemail and password == adminpass:
                request.session['admin_email'] = adminemail
                return redirect('admin_dashboard')
            
            print("Email:", email)
            print("Password:", password)
            
            user = User.objects.filter(Email=email, Password=password).first()
            print("User:", user)

            if user:
                if user.Role == 'Student':
                    request.session['user_id'] = user.id
                    return redirect('Student_Dashboard')
                elif user.Role == 'Teacher':
                    request.session['user_id'] = user.id
                    return redirect('Teacher_Dashboard')
                else:
                    return redirect('landing_page')
                
            else:
                print("No user found, returning HttpResponse...")
                return HttpResponse("Invalid Email or Password, Please register")
        else:
            print("Form not valid")
            return render(request, 'signup_login.html', {"login_form": login_form})
    
    return render(request, 'signup_login.html', {"login_form": login_form})

# admin dashboard
def admin_dashboard(request):
    admin_email = request.session.get('admin_email')
    if admin_email:
        teacher_details = TeacherProfile.objects.all()
        total_teachers = teacher_details.count()
        
        student_all = StudentProfile.objects.all()
        total_student = student_all.count() #count student
        recent_student = student_all.order_by('-id')[:5]
        department_detail = Department.objects.all()
        total_deparments = department_detail.count() # count department 
        new_department = department_detail.all().order_by('-id')[:5] # new departments
        total_new_deparment = new_department.count() # count new department
        return render(request,'admin_dashboard.html',{"admin_dashboard":"admin_dashboard","teacher_details":teacher_details,"department_detail":department_detail,"total_deparments":total_deparments,"total_new_deparment":total_new_deparment,"total_teachers":total_teachers,"total_student":total_student,"student_all":student_all,"recent_student":recent_student})
    else:
        return redirect('log_in')

# manage teachers
def manage_teachers(request):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect('log_in')
    

    search_query = request.GET.get('search','')

    if search_query:
        all_teachers = TeacherProfile.objects.filter(Q(name__icontains=search_query) | Q(department__name__icontains = search_query))
    else:
        all_teachers = TeacherProfile.objects.all()

    return render(request,'admin_dashboard.html',{"manage_teachers":"manage_teachers","all_teachers":all_teachers})
 
#  add teacher
def add_teachers(request):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect('log_in')    
    
    if request.method == 'POST':
        add_teacher_form = TeacherProfileForm(request.POST,request.FILES)
        user_email = request.POST.get('email')

        if add_teacher_form.is_valid():
            user = User.objects.create(
                Name=add_teacher_form.cleaned_data.get('name'),
                Email = user_email,
                Role = "Teacher",
                Password = add_teacher_form.cleaned_data.get('password')
            )

            teacher_profile = add_teacher_form.save(commit=False)
            teacher_profile.teacher = user
            teacher_profile.save()

            return redirect('manage_teachers')
        else:
            return render(request,"admin_dashboard.html",{"add_teacher_form":add_teacher_form})    
    else:
        add_teacher_form = TeacherProfileForm()
    
    return render(request,"admin_dashboard.html",{"add_teacher_form":add_teacher_form})

# edit teacher
def edit_teacher(request, pk):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect('log_in') 
    
    teacher_profile = TeacherProfile.objects.get(id=pk)

    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, request.FILES, instance=teacher_profile)

        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            user = teacher_profile.teacher

            # Check if email already exists for another user
            if User.objects.exclude(id=user.id).filter(Email=user_email).exists():
                form.add_error('email', 'This email is already taken by another user.')
                return render(request, "admin_dashboard.html", {"edit_teacher_form": form})

            # Update User object
            user.Name = form.cleaned_data.get('name')
            user.Email = user_email
            user.Password = form.cleaned_data.get('password')  #
            user.save()

            # Update TeacherProfile
            updated_profile = form.save(commit=False)
            updated_profile.teacher = user
            updated_profile.save()

            return redirect('manage_teachers')
        else:
            return render(request, "admin_dashboard.html", {"edit_teacher_form": form})
    else:
        form = TeacherProfileForm(instance=teacher_profile)
        # Pre-fill email & password from User
        form.initial['email'] = teacher_profile.teacher.Email
        form.initial['password'] = teacher_profile.teacher.Password
    
    return render(request, "admin_dashboard.html", {"edit_teacher_form": form})

# delete teacher
def delete_teacher(request,pk):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect('log_in')
    
    teacher_profile = TeacherProfile.objects.get(id=pk)
    teacher_profile.delete()

    return redirect('manage_teachers')


# manage department
def department(request):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect('log_in')
    
    search_query = request.GET.get('search', '')
    
    if search_query:
        department_detail = Department.objects.filter(
            Q(name__icontains=search_query) | Q(code__icontains=search_query)
        )
    else:
        department_detail = Department.objects.all()
    
    return render(request, 'admin_dashboard.html', {
        "department": "department",
        "department_detail": department_detail,
        "search_query": search_query
    })

# add department
def add_department(request):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect('log_in')
    
    if request.method == 'POST':
        department_form = DepartmentForm(request.POST)
        if department_form.is_valid():
            department_form.save()
            return redirect('department')
        else:
            return render(request,'admin_dashboard.html',{"department_form":department_form})
    else:
        department_form = DepartmentForm()

    return render(request,'admin_dashboard.html',{"department_form":department_form})

# edit department
def edit_department(request, pk):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect('log_in')
    
    # Get single object
    dept = Department.objects.get(id=pk)
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=dept)
        if form.is_valid():
            form.save()  # updates existing object
            return redirect('department')
    else:
        form = DepartmentForm(instance=dept)
    
    return render(request, 'admin_dashboard.html', {"department_form_edit": form})

# delete department
def delete_department(request,pk):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect('log_in')    
    
    dept = Department.objects.get(id=pk)
    dept.delete()

    return redirect('department')
    
# manage students
def manage_students(request):
    # Check role (admin/teacher)
    admin_email = request.session.get('admin_email')
    # If Admin
    if admin_email:
        all_students = StudentProfile.objects.all()
    else:
        return redirect('log_in')
    # search filter
    search_query = request.GET.get('search', '')
    if search_query:
        all_students = all_students.filter(
            Q(name__icontains=search_query) |
            Q(roll_number__icontains=search_query) |
            Q(department__name__icontains=search_query)
        )
    return render(request, 'admin_dashboard.html', {
        "manage_students": "manage_students",
        "all_students": all_students,
    })

# add student
def add_student(request):
    admin_email = request.session.get('admin_email')
    user_id = request.session.get('user_id')

    if not admin_email and not user_id:
        return redirect('log_in')

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create(
                Name=form.cleaned_data.get('name'),
                Email=form.cleaned_data.get('email'),
                Contact=form.cleaned_data.get('contact'),
                Role="Student",
                Password=form.cleaned_data.get('password')
            )
            student_profile = form.save(commit=False)
            student_profile.student = user
            student_profile.save()
            return redirect('manage_students')
    else:
        form = StudentProfileForm()

    return render(request, "admin_dashboard.html", {"student_form": form})

# edit student
def edit_student(request, pk):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect('log_in') 
    
    student_profile = StudentProfile.objects.get(id=pk)

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student_profile)

        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            user = student_profile.student   # yaha StudentProfile se related User nikala

            # Check if email already exists for another user
            if User.objects.exclude(id=user.id).filter(Email=user_email).exists():
                form.add_error('email', 'This email is already taken by another user.')
                return render(request, "admin_dashboard.html", {"edit_student_form": form})

            # Update User object
            user.Name = form.cleaned_data.get('name')
            user.Email = user_email
            user.Password = form.cleaned_data.get('password')  # plain rakha jaisa teacher me tha
            user.save()

            # Update StudentProfile
            updated_profile = form.save(commit=False)
            updated_profile.student = user
            updated_profile.save()

            return redirect('manage_students')
        else:
            return render(request, "admin_dashboard.html", {"edit_student_form": form})
    else:
        form = StudentProfileForm(instance=student_profile)
        # Pre-fill email & password from User
        form.initial['email'] = student_profile.student.Email
        form.initial['password'] = student_profile.student.Password
    
    return render(request, "admin_dashboard.html", {"edit_student_form": form})

# delete student
def delete_student(request, pk):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect('log_in')

    student_profile = StudentProfile.objects.get(id=pk)
    user = student_profile.student  # OneToOne link with User

    # pehle StudentProfile delete karo
    student_profile.delete()

    # fir linked User bhi delete kardo
    user.delete()

    return redirect('manage_students')

# Student Dashboard 
def Student_Dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('log_in')

    student = User.objects.filter(id=user_id, Role="Student").first()
    if not student:
        return HttpResponse("User not found or not a student")

    student_profile = StudentProfile.objects.filter(student=student).first()
    form = None

    if not student_profile:
        # Form show or submit
        if request.method == 'POST':
            form = StudentForm(request.POST, request.FILES)
            if form.is_valid():
                student_profile = form.save(commit=False)
                student_profile.student = student
                student_profile.save()
                # redirect to GET to avoid refresh on submit
                return redirect('Student_Dashboard')
            # Agar form invalid ho toh template me render karenge
        else:
            form = StudentForm()
        return render(request, 'student_dashboard.html', {"form": form})

    # Agar profile exist karta hai
    data = {
        "profile_id": student_profile.id,
        "student_id": student_profile.student.id,
        "name": student_profile.name,
        "email": student_profile.student.Email,
        "contact": student_profile.student.Contact,
        "profile": student_profile.profile_image,
        "course": student_profile.course,
        "year": student_profile.year,
        "roll_no": student_profile.roll_number,
        "department":student_profile.department,
    }
    return render(request, 'student_dashboard.html', {"dashboard":"dashboard","data": data})


# teacher dashboard
def Teacher_Dashboard(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("log_in")

    teacher = User.objects.filter(id=user_id, Role="Teacher").first()
    if not teacher:
        return HttpResponse("User not found or not a teacher")

    teacher_profile = TeacherProfile.objects.filter(teacher=teacher).first()

    if not teacher_profile:
        if request.method == "POST":
            form = TeacherProfileForm(request.POST, request.FILES)

            #  Remove unuse fields
            form.fields.pop('email', None)
            form.fields.pop('password', None)

            if form.is_valid():
                teacher_profile = form.save(commit=False)
                teacher_profile.teacher = teacher
                teacher_profile.save()
                return redirect("Teacher_Dashboard")
        else:
            form = TeacherProfileForm()
            form.fields.pop('email', None)
            form.fields.pop('password', None)

        return render(request, "teacher_dashboard.html", {"form": form})
    all_students = StudentProfile.objects.filter(department=teacher_profile.department)
    
    data = {
        "teacher_profile":teacher_profile,
        "name": teacher_profile.name,
        "designation": teacher_profile.designation,
        "department": teacher_profile.department,
        "total_departments":Department.objects.all().count(),
        "total_students":all_students.count(),
        "recent_students":all_students.order_by('-id')[:5],
        "all_students":all_students,
        "profile_image": teacher_profile.profile_image,
    }
    return render(request, "teacher_dashboard.html", {"dashboard": "dashboard","data": data})

    

# manage student for teacher
def manage_students_teacher(request):
    user_id = request.session.get('user_id')
    
    # If Teacher
    if user_id:
        teacher = User.objects.filter(id=user_id, Role="Teacher").first()
        if not teacher:
            return redirect('log_in')

        teacher_profile = TeacherProfile.objects.filter(teacher=teacher).first()
        if not teacher_profile:
            return HttpResponse("Teacher profile not found")

        # sirf teacher ke department ke students dikhana
        all_students = StudentProfile.objects.filter(department=teacher_profile.department)
    else:
        return redirect('log_in')
    # search filter
    search_query = request.GET.get('search', '')
    if search_query:
        all_students = all_students.filter(
            Q(name__icontains=search_query) |
            Q(roll_number__icontains=search_query) |
            Q(department__name__icontains=search_query)
        )
    return render(request, 'teacher_dashboard.html', {
        "manage_students": "manage_students",
        "all_students": all_students,
    })

# edit student by teacher
def edit_student_teacher(request, pk):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('log_in')

    teacher = User.objects.filter(id=user_id, Role="Teacher").first()
    if not teacher:
        return redirect('log_in')

    teacher_profile = TeacherProfile.objects.filter(teacher=teacher).first()
    if not teacher_profile:
        return HttpResponse("Teacher profile not found")

    student_profile = StudentProfile.objects.get(id=pk)

    # check student department (teacher sirf apne dept ke students edit kare)
    if student_profile.department != teacher_profile.department:
        return HttpResponse("You are not allowed to edit this student.")

    if request.method == 'POST':
        form = StudentProfileFormTeacher(request.POST, request.FILES, instance=student_profile)

        if form.is_valid():
            form.save()
            return redirect('manage_students_teacher')
        else:
            return render(request, "teacher_dashboard.html", {"edit_student_teacher_form": form})
    else:
        form = StudentProfileFormTeacher(instance=student_profile)

    return render(request, "teacher_dashboard.html", {
        "edit_student_teacher_form": form
    })

# delete student by teacher
def delete_student_teacher(request, pk):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('log_in')

    teacher = User.objects.filter(id=user_id, Role="Teacher").first()
    if not teacher:
        return redirect('log_in')

    teacher_profile = TeacherProfile.objects.filter(teacher=teacher).first()
    if not teacher_profile:
        return HttpResponse("Teacher profile not found")

    student_profile = StudentProfile.objects.get(id=pk)

    # check student department (teacher can only delete their dept students)
    if student_profile.department != teacher_profile.department:
        return HttpResponse("You are not allowed to delete this student.")

    student_profile.delete()
    
    return redirect('manage_students_teacher')


# My Profile 
def my_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('log_in')

    student = User.objects.filter(id=user_id, Role="Student").first()
    if not student:
        return HttpResponse("User not found or not a student")

    student_profile = StudentProfile.objects.filter(student=student).first()
    if student_profile:
        data = {
            "profile_id": student_profile.id,           # StudentProfile ki id
            "student_id": student_profile.student.id,   # User ki id
            "name": student_profile.name,
            "email": student_profile.student.Email,
            "contact": student_profile.student.Contact,
            "profile": student_profile.profile_image,
            "course": student_profile.course,
            "department":student_profile.department.name,
            "year": student_profile.year,
            "roll_no": student_profile.roll_number,
        }
        return render(request, "student_dashboard.html", {
            "my_profile_card": "my_profile_card",
            "data": data
        })

    return HttpResponse('<h1>Please Fill Your profile form</h1>')


# my profile for teacher
def my_profile_teacher(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('log_in')

    # Check if user is a teacher
    teacher = User.objects.filter(id=user_id, Role="Teacher").first()
    if not teacher:
        return HttpResponse("User not found or not a teacher")

    # Fetch teacher profile
    teacher_profile = TeacherProfile.objects.filter(teacher=teacher).first()
    if teacher_profile:
        data = {
            "profile_id": teacher_profile.id,            # TeacherProfile ki id
            "teacher_id": teacher_profile.teacher.id,    # User ki id
            "name": teacher_profile.name,
            "email": teacher_profile.teacher.Email,
            "contact": teacher_profile.teacher.Contact,
            "profile": teacher_profile.profile_image,
            "department": teacher_profile.department.name,
        }
        print(data)
        return render(request, "teacher_dashboard.html", {
            "my_profile_card": "my_profile_card",
            "data": data
        })

    return HttpResponse('<h1>Please Fill Your profile form</h1>')

# edit teacher my profile 
def edit_my_profile_teacher(request, pk):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('log_in')

    # direct filter with first()
    edit_profile = TeacherProfile.objects.filter(id=pk).first()
    if not edit_profile:
        return HttpResponse("Teacher Profile not found")

    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, request.FILES, instance=edit_profile)
        if form.is_valid():
            form.save()
            return redirect('my_profile_teacher')   # teacher profile view pe redirect karega
    else:
        form = TeacherProfileForm(instance=edit_profile)

    return render(request, 'teacher_dashboard.html', {
        "my_profile_edit_form": form
    })


# edit my profile
def edit_my_profile(request, pk):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('log_in')

    # direct filter with first()
    edit_profile = StudentProfile.objects.filter(id=pk).first()
    if not edit_profile:
        return HttpResponse("Profile not found")

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=edit_profile)
        if form.is_valid():
            form.save()
            return redirect('my_profile')   # profile view pe redirect karega
    else:
        form = StudentProfileForm(instance=edit_profile)

    return render(request, 'student_dashboard.html', {
        "my_profile_edit_form": form
    })

# help
def help_section(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('log_in')
    

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        subject = f"Help Request from {name}"
        full_message = f"From: {name}\nEmail: {email}\n\nMessage:\n{message}"

        send_mail(
            subject,
            full_message, #msg
            email,          # from
            ['ayushrusiya386@gmail.com'], # to
            fail_silently=False,
        )
        return HttpResponse("<h4>Message Sent Successfully!</h4>")

    return render(request, "student_dashboard.html", {"help_form": "help_form"})

# ebooks list
def ebook_list(request):
    user_id = request.session.get('admin_email')
    if not user_id:
        return redirect('log_in')
    
    ebooks = EBook.objects.all()

    # search filter
    search_query = request.GET.get('search', '')

    if search_query:
        ebooks = ebooks.filter(Q(title__icontains=search_query))

    return render(request,'admin_dashboard.html',{"ebooks":ebooks,"ebook_list":"ebook_list"})


# Teacher view
def ebook_list_teacher(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('log_in')

    teacher = User.objects.filter(id=user_id, Role="Teacher").first()
    if not teacher:
        return redirect('log_in')

    teacher_profile = TeacherProfile.objects.filter(teacher=teacher).first()
    if not teacher_profile:
        return HttpResponse("Teacher profile not found")

    # books
    ebooks = EBook.objects.all()

    # search filter
    search_query = request.GET.get('search', '')
    if search_query:
        ebooks = ebooks.filter(Q(title__icontains=search_query))

    return render(request, 'teacher_dashboard.html', {"ebooks": ebooks, "ebook_list": "ebook_list_teacher"})


# Student view
def ebook_list_student(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('log_in')

    student = User.objects.filter(id=user_id, Role="Student").first()
    if not student:
        return redirect('log_in')

    student_profile = StudentProfile.objects.filter(student=student).first()
    if not student_profile:
        return HttpResponse("Student profile not found")
    data = {
            "name": student_profile.name,
        }

    # all books for student
    ebooks = EBook.objects.all()

    # search filter
    search_query = request.GET.get('search', '')
    if search_query:
        ebooks = ebooks.filter(Q(title__icontains=search_query))

    # session based read later
    read_later_ids = request.session.get('read_later_list', [])
    read_later_length = len(read_later_ids)

    return render(
        request,
        'student_dashboard.html',
        {
            "ebooks": ebooks,
            "read_later_ids":read_later_ids,
            "ebook_list": "ebook_list_student",
            "read_later_length": read_later_length,  # read leter book count ke liye
            "data":data,
        }
    )


# upload ebooks
def upload_ebooks(request):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect('log_in') 
    
    if request.method == 'POST':
        form = EbookForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ebook_list')
        else:
            return render(request,"admin_dashboard.html",{"form":form})
    else:
        form = EbookForm()
        return render(request,"admin_dashboard.html",{"form":form})
    
# delete ebooks
def delete_ebook(request,pk):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect('log_in')
    
    book = EBook.objects.get(id=pk)
    book.delete()
    
    return redirect('ebook_list')

# edit books
def edit_book(request, pk):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect('log_in')

    book = EBook.objects.get(id=pk)
    if request.method == "POST":
        form = EbookForm(request.POST, request.FILES, instance=book) 
        if form.is_valid():
            form.save()
            return redirect('ebook_list')
    else:
        form = EbookForm(instance=book)
    return render(request, "admin_dashboard.html", {"form": form})


# Toggle add/remove
def toggle_read_later(request, pk):
    read_later_list = request.session.get('read_later_list', [])

    if pk in read_later_list:
        read_later_list.remove(pk)
    else:
        read_later_list.append(pk)

    request.session['read_later_list'] = read_later_list

    return redirect('ebook_list_student')   # back to main list

# Read Later list page
def read_later_list(request):
    read_later_ids = request.session.get('read_later_list', [])
    ebooks = EBook.objects.filter(id__in=read_later_ids)   #  correct filter
    read_later_length = len(read_later_ids)                #  correct length

    return render(
        request,
        'student_dashboard.html', 
        {
            'read_leter_ebooks': ebooks,
            'read_later_length': read_later_length,
            'read_later_ids': read_later_ids
        }
    )

# log out for all 
def log_out(request):
    # admin ke liye
    if 'admin_email' in request.session:
        del request.session['admin_email']
        return redirect('landing_page')
    elif 'user_id' in request.session:
        del request.session['user_id']
        return redirect('landing_page')
