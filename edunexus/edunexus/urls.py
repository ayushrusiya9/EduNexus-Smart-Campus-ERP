"""
URL configuration for edunexus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app_edunexus import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('',views.landing_page,name='landing_page'),
    path('about/',views.about,name='about'),
    path('why_choose_us/',views.why_choose_us,name='why_choose_us'),
    path('contact',views.contact,name='contact'),

    path('sign_up',views.sign_up,name='sign_up'),
    path('log_in/',views.log_in,name='log_in'),
    path('log_out/',views.log_out,name='log_out'),

    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),

    path('admin_dashboard/announcements/', views.announcement_list, name='announcement_list'),
    path('admin_dashboard/announcements/add/', views.announcement_create, name='announcement_create'),
    path('admin_dashboard/announcements/edit/<int:pk>/', views.announcement_update, name='announcement_update'),
    path('admin_dashboard/announcements/delete/<int:pk>/', views.announcement_delete, name='announcement_delete'),

    path('admin_dashboard/manage_teachers/',views.manage_teachers,name='manage_teachers'),
    path('admin_dashboard/manage_teachers/add_teachers/',views.add_teachers,name='add_teachers'),
    path('admin_dashboard/manage_teachers/edit_teacher/<int:pk>/',views.edit_teacher,name='edit_teacher'),
    path('admin_dashboard/manage_teachers/delete_teacher/<int:pk>/',views.delete_teacher,name='delete_teacher'),

    path('admin_dashboard/manage_students/',views.manage_students,name='manage_students'),
    path('admin_dashboard/manage_students/add_student/',views.add_student,name='add_student'),
    path('admin_dashboard/manage_students/edit_student/<int:pk>/',views.edit_student,name='edit_student'),
    path('admin_dashboard/manage_students/delete_student/<int:pk>/',views.delete_student,name='delete_student'),

    path('admin_dashboard/department/',views.department,name='department'),
    path('admin_dashboard/department/add_department/',views.add_department,name='add_department'),
    path('admin_dashboard/department/edit_department/<int:pk>/',views.edit_department,name='edit_department'),
    path('admin_dashboard/department/delete_department/<int:pk>/',views.delete_department,name='delete_department'),

    path('admin_dashboard/department/E_library/',views.ebook_list,name='ebook_list'),
    path('admin_dashboard/department/E_library/upload_ebooks/',views.upload_ebooks,name='upload_ebooks'),
    path('admin_dashboard/department/E_library/edit_book/<int:pk>/',views.edit_book,name='edit_book'),
    path('admin_dashboard/department/E_library/delete_ebook/<int:pk>/',views.delete_ebook,name='delete_ebook'),

    path('Student_Dashboard/',views.Student_Dashboard,name='Student_Dashboard'),

    path('Student_Dashboard/My_profile/',views.my_profile,name='my_profile'),
    path('Student_Dashboard/My_profile/edit_my_profile/<int:pk>/',views.edit_my_profile,name='edit_my_profile'),
    path('Student_Dashboard/ebook_list_student/',views.ebook_list_student,name='ebook_list_student'),
    path('Student_Dashboard/read_later_list/',views.read_later_list,name='read_later_list'),
    path('Student_Dashboard/toggle_read_later/<int:pk>/',views.toggle_read_later,name='toggle_read_later'),
    path('Student_Dashboard/Help/',views.help_section,name='help_section'),


    path('Teacher_Dashboard/',views.Teacher_Dashboard,name='Teacher_Dashboard'),
    
    path('Teacher_Dashboard/my_profile_teacher/',views.my_profile_teacher,name='my_profile_teacher'),
    path('Teacher_Dashboard/edit_my_profile_teacher/<int:pk>/',views.edit_my_profile_teacher,name='edit_my_profile_teacher'),
    path('manage_students_teacher',views.manage_students_teacher,name='manage_students_teacher'),
    path('manage_students_teacher/edit_student_teacher/<int:pk>/',views.edit_student_teacher,name='edit_student_teacher'),
    path('manage_students_teacher/delete_student_teacher/<int:pk>/',views.delete_student_teacher,name='delete_student_teacher'),
    path('Teacher_Dashboard/ebook_list',views.ebook_list_teacher,name='ebook_list_teacher'),
]
