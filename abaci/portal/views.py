from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin #requires a login to access page
from django import forms
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from .models import clss, topic
from .forms import CustomCreateView, CustomUpdateView, CustomTopicCreateView
from django.urls import reverse_lazy
import random

class ClssListView(LoginRequiredMixin, ListView):
    template_name = 'teacher/portal.html'
    context_object_name = 'classes'
    ordering = ['name']

    def get_queryset(self):
        return clss.objects.filter(teacher=self.request.user)#only pass in classes owned by logged in teacher

    def get_context_data(self, **kwargs):#show topics within the class
        context = super(ClssListView, self).get_context_data(**kwargs)
        context['topics']=[]
        for i in clss.objects.filter(teacher=self.request.user):
            for t in topic.objects.filter(Clss=i):
                if t.live == True:
                    context['topics'].append(t)#add active topic to list
        return context


class ClssDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = clss
    template_name = 'teacher/clss.html'
    context_object_name = 'clss'

    def test_func(self):#ensure they own this class
        Clss = self.get_object()
        if self.request.user == Clss.teacher:
            return True
        else:
            return False

    def get_context_data(self, **kwargs):#show topics within the class
        context = super(ClssDetailView, self).get_context_data(**kwargs)
        context['topics'] = topic.objects.filter(Clss=clss.objects.get(ID=self.get_object().ID))#get topics associated with this class
        for i in context['topics']:
            i.total = i.green+i.amber+i.red
        return context

class ClssCreateView(LoginRequiredMixin, CustomCreateView):
    model = clss
    template_name = 'teacher/create.html'
    fields = ['name']#only require name everything else can be filled in

    def form_valid(self, form):#edit form submit data to add teacher and gen class id
        form.instance.teacher = self.request.user#sets teacher to the currently logged in user
        form.instance.ID=random.randint(111111,999999)
        while clss.objects.filter(ID=form.instance.ID).exists():#loops until found unique class id
            form.instance.ID=random.randint(111111,999999)
        return super().form_valid(form) #saves class

class ClssDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = clss
    template_name='teacher/delete.html'
    success_url="/portal"

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
            i.live = False
            i.save()
        form.instance.live = True #topic is live
        return super().form_valid(form) #saves class



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
