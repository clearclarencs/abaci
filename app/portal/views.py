from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin #requires a login to access page
from django import forms
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from .models import clss, topic, comment
from .forms import CustomCreateView, CustomTopicCreateView
from django.urls import reverse_lazy
import random
'''PORTAL APP, VIEWS, Classes for different pages in teacher portal IMAGE 1/2'''
class ClssListView(LoginRequiredMixin, ListView):
    template_name = 'teacher/portal.html'
    context_object_name = 'classes'
    ordering = ['name']

    def get_queryset(self):
        classes = clss.objects.filter(teacher=self.request.user) # #only pass in classes owned by logged in teacher
        for clas in classes:
            added = False
            for t in topic.objects.filter(Clss=clas):
                if t.live == True:
                    clss.label = f'<h2 id="topic" style="color:#4CBB17">{t}</h2>' # add active topic to list
                    added = True
            if not added:
                clas.label = '''<h2 id="topic" style="color:#E60000">No active topic</h2>''' # if no active topic
        return classes


class ClssDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = clss
    template_name = 'teacher/clss.html'
    context_object_name = 'clss'

    def test_func(self): # ensure they own this class
        Clss = self.get_object()
        if self.request.user == Clss.teacher:
            return True
        else:
            return False

    def get_context_data(self, **kwargs): # show topics within the class
        context = super(ClssDetailView, self).get_context_data(**kwargs)
        context['topics'] = topic.objects.filter(Clss=clss.objects.get(ID=self.get_object().ID)) # get topics associated with this class
        for i in context['topics']:
            i.total = i.green+i.amber+i.red # Topic total as if 0 shows no responses submitted
        return context

class ClssCreateView(LoginRequiredMixin, CustomCreateView):
    model = clss
    template_name = 'teacher/create.html'
    fields = ['name']#only require name everything else can be filled in

    def form_valid(self, form):#edit form submit data to add teacher and gen class id
        form.instance.teacher = self.request.user#sets teacher to the currently logged in user
        form.instance.ID=random.randint(111111,999999)
        while clss.objects.filter(ID=form.instance.ID).exists():#loops until found unique class id
            form.instance.ID=random.randint(111111,999999) # get unused id
        return super().form_valid(form) #saves class
'''PORTAL APP, VIEWS, Classes for different pages in teacher portal IMAGE 2/2'''
class ClssDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = clss
    template_name='teacher/delete.html'
    success_url="/portal" # redirect url

    def test_func(self):
        Clss = self.get_object()
        if self.request.user == Clss.teacher:
            return True
        else:
            return False


class TopicCreateView(LoginRequiredMixin, CustomTopicCreateView):
    model = topic
    template_name = 'teacher/topiccreate.html'
    fields = ['title']#only require name everything else can be filled in

    def form_valid(self, form):#edit form submit data to add teacher and gen class id
        form.instance.Clss = clss.objects.filter(pk=self.kwargs['pk']).first()#get class for which the topic will be part of
        return super().form_valid(form) #saves class

class TopicUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):#Used to activate topic
    model = topic
    template_name = 'teacher/topicupdate.html'
    fields=[]

    def test_func(self):
        topic = self.get_object()
        if self.request.user == topic.Clss.teacher:
            return True
        else:
            return False

    def form_valid(self, form):#edit form submit data to add teacher and gen class id
        othertopics = topic.objects.filter(Clss=form.instance.Clss)
        for i in othertopics:
            i.live = False # Deactivate other topics
            i.save()
        form.instance.live = True #topic is live
        return super().form_valid(form) #saves class

    def get_context_data(self, **kwargs):#show topics within the class
        context = super(TopicUpdateView, self).get_context_data(**kwargs)
        context['comments'] = comment.objects.filter(topic=self.get_object()).values_list('body', flat=True)
        #get topics associated with this class
        return context




class TopicDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = topic
    template_name='teacher/topicdelete.html'

    def test_func(self):
        topic = self.get_object()
        if self.request.user == topic.Clss.teacher:
            return True
        else:
            return False
    
    def get_success_url(self):
        return reverse_lazy('clss-detail', kwargs={'pk': self.object.Clss.ID})


'''
CLASS
TopicUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView)
    model ← topic
    template_name ← 'teacher/topicupdate.html'
    fields ← []

    SUBROUTINE
    test_func(self):
        topic ← self.get_object()
        IF self.request.user ← topic.Clss.teacher THEN
            RETURN True
        ELSE THEN
            RETURN False
    ENDSUBROUTINE

    SUBROUTINE
    form_valid(self, form)
        othertopics ← topic.objects.filter(Clss=form.instance.Clss)
        FOR i ← IN othertopics
            i.live ← False
            i.save()
        form.instance.live = True #topic is live
        RETURN super().form_valid(form) #saves class

    SUBROUTINE
    get_context_data(self, **kwargs)
        context ← super(TopicUpdateView, self).get_context_data(**kwargs)
        context['comments'] ← comment.objects.filter(topic=self.get_object()).values_list('body', flat=True)#get topics associated with this class
        RETURN context
    ENDSUBROUTINE 
ENDCLASS
'''