from django import forms
from django.core.exceptions import ValidationError
from .models import User, StudentProfile, TeacherProfile, Department,EBook,Announcement


# SIGNUP FORM
from django import forms
from django.core.exceptions import ValidationError
from .models import User   # Apne model ka path confirm kar lena


class SignupForm(forms.ModelForm):
    ROLE_CHOICES = [
        ("Student", "Student"),
        ("Teacher", "Teacher")
    ]

    # Fields with required=False + Bootstrap widgets
    Name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter Name'})
    )

    Email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter Email'})
    )

    Contact = forms.CharField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter Contact'})
    )

    Role = forms.ChoiceField(
        required=False,
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control mb-3'})
    )

    Password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter Password'})
    )

    Confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ["Name", "Email", "Contact", "Role", "Password"]

    # Field Validations 
    def clean_Name(self):
        name = self.cleaned_data.get("Name")
        if not name:
            raise ValidationError("Please enter your name")
        elif name.isdigit():
            raise ValidationError("Name should not be only numbers")
        elif not name.replace(" ", "").isalpha():
            raise ValidationError("Name should only contain letters")
        return name

    def clean_Email(self):
        email = self.cleaned_data.get("Email")
        if not email:
            raise ValidationError("Please enter your email")
        elif not email.endswith("@gmail.com"):
            raise ValidationError("Email must be a valid Gmail address")
        return email

    def clean_Contact(self):
        contact = self.cleaned_data.get("Contact")
        if not contact:
            raise ValidationError("Please enter your contact number")
        elif len(str(contact)) != 10:
            raise ValidationError("Contact number must be 10 digits")
        elif not str(contact).isdigit():
            raise ValidationError("Contact must contain only numbers")
        return contact

    def clean_Password(self):
        password = self.cleaned_data.get("Password")
        if not password:
            raise ValidationError("Please enter a password")
        elif len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        elif password.isdigit():
            raise ValidationError("Password should not be only numbers")
        return password

    def clean_Role(self):
        role = self.cleaned_data.get("Role")
        if not role:
            raise ValidationError("Please select a role")
        return role

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("Password")
        confirm_password = cleaned_data.get("Confirm_password")

        if not confirm_password:
            raise ValidationError("Please confirm your password")
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Confirm Passwords not match")


class LoginForm(forms.Form):
    Email = forms.EmailField(
        widget=forms.EmailInput(attrs={ 
            'class': 'form-control mb-3', 
            'placeholder': 'Enter Email' 
        })
    ) 
    Password = forms.CharField(
        widget=forms.PasswordInput(attrs={ 
            'class': 'form-control mb-3', 
            'placeholder': 'Enter Password' 
        })
    ) 

# STUDENT PROFILE FORM
class StudentProfileForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Email'
        }),
        required=True,
        label="Email"
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password'
        }),
        min_length=6,
        required=True,
        label="Password"
    )

    contact = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Contact Number'
        }),
        required=True,
        label="Contact Number"
    )

    class Meta:
        model = StudentProfile
        fields = ['name', 'profile_image', 'course', 'year', 'roll_number', 'department', 'email', 'password', 'contact']

        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name'}),
            'course': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Course'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Year'}),
            'roll_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Roll Number'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
        }

    # FIELD VALIDATIONS
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name:
            raise ValidationError("Please enter your name")
        elif name.isdigit():
            raise ValidationError("Name should not be only numbers")
        elif not name.replace(" ", "").isalpha():
            raise ValidationError("Name should only contain letters")
        return name

    def clean_contact(self):
        contact = self.cleaned_data.get("contact")
        if not contact.isdigit():
            raise ValidationError("Contact number must contain only digits")
        if len(contact) != 10:
            raise ValidationError("Contact number must be 10 digits long")
        return contact

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(Email=email).exists():
            raise ValidationError("This email is already registered!")
        return email

    def clean_year(self):
        year = self.cleaned_data.get("year")
        if year <= 0 or year > 5:
            raise ValidationError("Year must be between 1 and 5")
        return year

    def clean_roll_number(self):
        roll = self.cleaned_data.get("roll_number")
        if not roll:
            raise ValidationError("Please enter Roll Number")
        if not roll.isalnum():
            raise ValidationError("Roll Number must be alphanumeric")
        return roll

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 6:
            raise ValidationError("Password must be at least 6 characters long")
        return password

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password'
        }),
        min_length=6
    )
    contact = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Contact Number'
        })
    )

    class Meta:
        model = StudentProfile
        fields = ['name', 'profile_image', 'course', 'year', 'roll_number', 'department']

        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name'}),
            'course': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Course'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Year'}),
            'roll_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Roll Number'}),
            'department': forms.Select(attrs={'class': 'form-control'})
        }

    #  FIELD VALIDATIONS
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name:
            raise ValidationError("Please enter your name")
        elif name.isdigit():
            raise ValidationError("Name should not be only numbers")
        elif not name.replace(" ", "").isalpha():
            raise ValidationError("Name should only contain letters")
        return name

    def clean_contact(self):
        contact = self.cleaned_data.get("contact")
        if not contact.isdigit():
            raise ValidationError("Contact number must contain only digits")
        if len(contact) != 10:
            raise ValidationError("Contact number must be 10 digits long")
        return contact

    def clean_year(self):
        year = self.cleaned_data.get("year")
        if year <= 0 or year > 5:
            raise ValidationError("Year must be between 1 and 5")
        return year

    def clean_roll_number(self):
        roll = self.cleaned_data.get("roll_number")
        if not roll:
            raise ValidationError("Please enter Roll Number")
        if not roll.isalnum():
            raise ValidationError("Roll Number must be alphanumeric")
        return roll

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 6:
            raise ValidationError("Password must be at least 6 characters long")
        return password


# ================= TEACHER PROFILE FORM ===================
class TeacherProfileForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
        required=True,
        label="Password"
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email Adddress'}),
        required=True,
        label="Email"
    )

    class Meta:
        model = TeacherProfile
        fields = ['name', 'profile_image', 'designation', 'department', 'password','email']  # include password

        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Teacher Name'}),
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Designation'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name:
            raise ValidationError("Please enter teacher name")
        elif name.isdigit():
            raise ValidationError("Name should not be only numbers")
        elif not name.replace(" ", "").isalpha():
            raise ValidationError("Name should only contain letters")
        return name


# ================= DEPARTMENT FORM ===================
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Department Name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Department Code'}),
        }


class EbookForm(forms.ModelForm):

    class Meta:
        model = EBook
        fields = ['title','description','file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter book description'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }    


class StudentProfileFormTeacher(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'name',
            'profile_image',
            'department',
            # aur jo bhi StudentProfile model me fields hain
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
        }


class StudentForm(forms.ModelForm):

    class Meta:
        model = StudentProfile
        fields = ['name', 'profile_image', 'course', 'year', 'roll_number', 'department']

        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name'}),
            'course': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Course'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Year'}),
            'roll_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Roll Number'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
        }



class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter title'}),
            'content': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Enter content','rows':4}),
        }