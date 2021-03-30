from django import forms
from django.contrib.auth.models import User#
from portal.models import topic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.urls import reverse_lazy
'''STUDENT APP, FORMS, page forms'''
class ClassLoginForm(forms.ModelForm):
    class_id = forms.CharField(max_length=6, widget=forms.TextInput(attrs={
        'placeholder': 'Class ID', 
        'type' : 'number',
        'max': '999999',
        'min': '111111'
        }))#class codes are 6 digits, sets html attributes
        
    class Meta:
        model=topic
        fields = ['class_id'] # Only 1 field

'''
CLASS
ClassLoginForm(forms.ModelForm)
    class_id ← forms.CharField(max_length ← 6, widget ← forms.TextInput(attrs ← {
        'placeholder': 'Class ID', 
        'type' : 'number',
        'max': '999999',
        'min': '111111'
        }))
        
    CLASS
    Meta()
        model ← topic
        fields ← ['class_id']
    ENDCLASS
ENDCLASS

'''
