from django import forms
from django.views.generic import CreateView, UpdateView

class CustomCreateView(CreateView):
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(CustomCreateView, self).get_form(form_class)
        form.fields['name'].widget = forms.TextInput(attrs={'placeholder': 'Name'})
        return form

class CustomTopicCreateView(CreateView):
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(CustomTopicCreateView, self).get_form(form_class)
        form.fields['title'].widget = forms.TextInput(attrs={'placeholder': 'Name'})
        return form

class CustomUpdateView(CreateView):
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(CustomUpdateView, self).get_form(form_class)
        form.fields['name'].widget = forms.TextInput(attrs={'placeholder': 'Name'})
        return form