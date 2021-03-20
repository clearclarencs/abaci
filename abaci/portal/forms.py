from django import forms
from django.views.generic import CreateView, UpdateView
'''PORTAL APP, FORMS, page forms for teacher portal'''
class CustomCreateView(CreateView): # Create class form
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(CustomCreateView, self).get_form(form_class)
        form.fields['name'].widget = forms.TextInput(attrs={'placeholder': 'Name'}) # Class name
        return form

class CustomTopicCreateView(CreateView): #Create topic form
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(CustomTopicCreateView, self).get_form(form_class)
        form.fields['title'].widget = forms.TextInput(attrs={'placeholder': 'Name'}) # Topic name
        return form

