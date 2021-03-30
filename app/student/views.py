from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin #requires a login to access page
from django import forms
from portal.models import clss, topic, comment
from django.http import HttpResponse
from .forms import ClassLoginForm
from django.contrib import messages
''' STUDENT APP, VIEWS, This page if for viewing any page as a student (home and vote page)'''
def home(request): # Home page + student login page
    if request.method=='POST':
        #username = email and is all lowercase
        form = ClassLoginForm(request.POST)
        if form.is_valid():
            return redirect('student-vote', class_id = form.cleaned_data['class_id']) # Redirect to vote page
    else:
        form = ClassLoginForm() # Give form to login if post
    return render(request, 'student/login.html', {'form':form})

def vote(request, class_id):
    try:
        topicobj = topic.objects.get(Clss=clss.objects.get(pk=class_id), live=True) # Gets live topic
    except clss.DoesNotExist:
        messages.error(request, f'Invalid class code')
        return redirect('student-home')
    except topic.DoesNotExist:
        messages.error(request, f'No active topic')
        return redirect('student-home')

    if request.method == 'POST':
        selected_option = request.POST
        if selected_option.get("comment") != None and selected_option.get("comment") != "":
            # Green will be None but amber/red will be "" if empty
            commentBody = selected_option.get("comment")
            c = comment(topic=topicobj, body=commentBody)
            c.save()
        if selected_option.get("green") != None: # Add a vote for the colour
            topicobj.green += 1
        elif selected_option.get("amber") != None:
            topicobj.amber += 1
        elif selected_option.get("red") != None:
            topicobj.red += 1
        else:
            return HttpResponse(400, 'Invalid choice') # Error message

        topicobj.save()

        messages.success(request, 'Response submitted!') # Success message
        return redirect('student-home')
    '''
    IF request.method = 'POST' THEN
        selected_option ← request.POST
        IF (selected_option.get("comment") ≠ None) AND (selected_option.get("comment") ≠ "") THEN # Green will be None but amber/red will be "" if empty
            commentBody ← selected_option.get("comment")
            c ← comment(topic←topicobj, body←commentBody)
            c.save() # Save the entity to 
        ENDIF
        IF selected_option.get("green") ≠ None THEN
            topicobj.green = topicobj.green + 1
        ELSE IF selected_option.get("amber") ≠ None THEN
            topicobj.amber = topicobj.amber + 1
        ELSE IF selected_option.get("red") ≠ None THEN
            topicobj.red = topicobj.red + 1
        ELSE THEN
            RETURN HttpResponse(400, 'Invalid choice') # Issue with choice so returns http 400 code
        ENDIF

        topicobj.save()

        messages.success(request, 'Response submitted!')
        RETURN redirect('student-home') # Redirect back home
    ENDIF
    '''

    context = {
        'topic' : topicobj
    }
    return render(request, 'student/submit.html', context)
