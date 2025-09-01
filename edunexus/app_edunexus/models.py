from django.db import models
from cloudinary_storage.storage import MediaCloudinaryStorage,RawMediaCloudinaryStorage

# Common User table
class User(models.Model):
    Name = models.CharField(max_length=50)
    Email = models.EmailField()
    Contact = models.CharField(max_length=15)  # +91... ke liye CharField better hai
    Role = models.CharField(max_length=20, choices=[("Student", "Student"), ("Teacher", "Teacher")])
    Password = models.CharField(max_length=100)

    class Meta:
        db_table = "User"

    def __str__(self):
        return self.Name


# Department Model (Student + Teacher dono ke liye)
class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = "Department"
        get_latest_by = "code"

    def __str__(self):
        return self.name


# Student Profile
class StudentProfile(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'Role': 'Student'})
    name = models.CharField(max_length=50)
    profile_image = models.ImageField(storage=MediaCloudinaryStorage, upload_to='students/')
    course = models.CharField(max_length=50)
    year = models.IntegerField()
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "Student_Profile"

    def __str__(self):
        return f"{self.name} roll no  {self.roll_number}"

# Teacher Profile
class TeacherProfile(models.Model):
    teacher = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'Role': 'Teacher'})
    name = models.CharField(max_length=50)
    profile_image = models.ImageField(storage=MediaCloudinaryStorage, upload_to='images/')
    designation = models.CharField(max_length=100)   # Assistant Professor, HOD
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "Teacher_Profile"

    def __str__(self):
        return f"{self.name} designation: {self.designation}"


# Ebooks
class EBook(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(storage=RawMediaCloudinaryStorage,upload_to="ebooks/")   # MEDIA folder me save hoga
    uploaded_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.title
    
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Announcement"

    def __str__(self):
        return self.title