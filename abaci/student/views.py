from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin #requires a login to access page
from django import forms
from portal.models import clss, topic
from django.http import HttpResponse
from .forms import ClassLoginForm
from django.contrib import messages

def home(request):
    if request.method=='POST':
        #username = email and is all lowercase
        form = ClassLoginForm(request.POST, instance=request.user)
        if form.is_valid():
            return redirect('student-vote', class_id = form.cleaned_data['class_id'])
    else:
        form = ClassLoginForm()
    return render(request, 'student/login.html', {'form':form})

def vote(request, class_id):
    try:
        topicobj = topic.objects.get(Clss=clss.objects.get(pk=class_id), live=True)
    except clss.DoesNotExist:
        messages.error(request, f'Invalid class code')
        return redirect('student-home')
    except topic.DoesNotExist:
        messages.error(request, f'No active topic')
        return redirect('student-home')

    if request.method == 'POST':
        selected_option = request.POST
        if 'green' in selected_option:
            topicobj.green += 1
        elif 'amber' in selected_option:
            topicobj.amber += 1
        elif 'red' in selected_option:
            topicobj.red += 1
        else:
            return HttpResponse(400, 'Invalid class')

        topicobj.save()

        messages.success(request, f'Response submitted!')
        return redirect('student-home')

    context = {
        'topic' : topicobj
    }
    return render(request, 'student/submit.html', context)
