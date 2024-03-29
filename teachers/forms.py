from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.forms.widgets import PasswordInput, TextInput
''' TEACHER APP, FORMS, This file is for any page forms associated with the teacher section which is account management so excludes any portal forms'''
class CustomAuthForm(AuthenticationForm):#Login custom auth form to insert placeholders, change input type and set js variables
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Email', 'type' : 'email', 'onkey' : 'return forceLower(this);'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'placeholder': 'Email', 
        'type' : 'email', 
        'onkey' : 'return forceLower(this);'
        }))#store email as username as username not required
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = None #No password confirmation

    class Meta:
        model = User
        fields = ('username', 'email', 'password1') # Need all fields but username and email will be users email

    def clean_password1(self): #So only 1 password input
        password1 = self.cleaned_data.get('password1')
        try:
            password_validation.validate_password(password1, self.instance)
        except forms.ValidationError as error:
            self.add_error('password1', error)
        return password1
    
    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['username'],#username is the email and is stored twice so stored under username and email
            self.cleaned_data['password1']
        )
        return user

class CustomPasswordUpdateForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'type': 'password', 
        'placeholder': 'Current Password', 
        'style':"border-color:#E60000;margin-bottom:60px;font-size:20px;"
        }))#edit placeholders
    new_password1 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'type': 'password', 
        'placeholder': 'New Password', 
        'style':"border-color:#FEAF00;font-size:20px;"
        }))
    new_password2 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'type': 'hidden', 
        'value': 'BLANK', 
        'placeholder': 'New Password', 
        'style':"border-color:#FEAF00"
        }))
    class Meta:
        model=User
        fields = ['old_password', 'new_password1']

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password1')
        password_validation.validate_password(new_password2, self.user)
        return new_password2

'''
CLASS
UserRegisterForm(UserCreationForm)
    username ← forms.CharField(
        max_length=200, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Email', 
            'type' : 'email', 
            'onkey' : 'return forceLower(this);'
            }
        )
    )#store email as username as username not required
    password1 ← forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 ← None #No password confirmation

    CLASS
    Meta()
        model ← User
        fields ← ('username', 'email', 'password1')
    ENDCLASS

    #So only 1 password input
    SUBROUTINE
    clean_password1(self)
        password1 ← self.cleaned_data.get('password1')
        TRY THEN
            password_validation.validate_password(password1, self.instance)
        EXCEPT error ← forms.ValidationError THEN
            self.add_error('password1', error)
        RETURN password1
    ENDSUBROUTINE

    SUBROUTINE
    save(self, commit=True)
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['username'],#username and password are duplicated so that both contain email
            self.cleaned_data['password1']
        )
        RETURN user
    ENDSUBROUTINE
ENDCLASS
'''

            
            

