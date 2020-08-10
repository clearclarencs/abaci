from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


class CustomAuthForm(AuthenticationForm):#Login custom auth form to insert placeholders, change input type and set js variables
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Email', 'type' : 'email', 'onkey' : 'return forceLower(this);'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Email', 'type' : 'email', 'onkey' : 'return forceLower(this);'}))#store email as username as username not required
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = None #No password confirmation

    class Meta:
        model = User
        fields = ('username', 'email', 'password1')

    #So only 1 password input
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        try:
            password_validation.validate_password(password1, self.instance)
        except forms.ValidationError as error:
            self.add_error('password1', error)
        return password1
    
    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['username'],#username and password are duplicated so that both contain email
            self.cleaned_data['password1']
        )
        return user

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Email', 'type' : 'email', 'onkey' : 'return forceLower(this);'}))#store email as username as username not required
    class Meta:
        model=User
        fields = ['username']
