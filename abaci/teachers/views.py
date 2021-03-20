from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, CustomPasswordUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views, update_session_auth_hash
'''TEACHER APP, VIEWS, This file is for any requests to the teacher account section including get requests and managing post requests.'''
def register(request):
    if request.user.is_authenticated: # redirects logged in users to portal
       return redirect('teacher-portal')
    else:
        if request.method == 'POST':
            #username = email and is all lowercase
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username=form.cleaned_data.get('username')
                messages.success(request, f'Account created for { username }, please login!')
                return redirect('login') # Must now login
            
        else:
            form = UserRegisterForm() # Form for get request
        return render(request, 'teachers/register.html', {'form':form}) #passes form and webpage and renders

@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomPasswordUpdateForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) # Hash password passing in the form in request
            messages.success(request, 'Password updated!')
            return redirect('login') # Relogin
        else:
            messages.error(request, '')
    else:
        form = CustomPasswordUpdateForm(request.user)
    return render(request, 'teachers/profile.html', {
        'form': form
    })

'''
SUBROUTINE
register(request)
    IF request.user.is_authenticated THEN
       RETURN redirect('teacher-portal')
    ELSE THEN
        IF request.method = 'POST' THEN
            form ← UserRegisterForm(request.POST)
            IF form.is_valid() THEN
                form.save()
                username ← form.cleaned_data.get('username')
                messages.success(request, f'Account created for { username }, please login!')
                return redirect('login')
            ENDIF
        ELSE THEN
            form ← UserRegisterForm()
        RETURN render(request, 'teachers/register.html', {'form':form})
        ENDIF
    ENDIF
ENDSUBROUTINE

@login_required # A static method to ensure user is logged in
SUBROUTINE
profile(request)
    IF request.method = 'POST' THEN
        form ← CustomPasswordUpdateForm(request.user, request.POST)
        IF form.is_valid() THEN
            user ← form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated!')
            RETURN redirect('login')
        ELSE THEN
            messages.error(request, 'Error')
        ENDIF
    ELSE THEN
        form ← CustomPasswordUpdateForm(request.user)
    ENDIF
    RETURN render(request, 'teachers/profile.html', {'form': form})
ENDSUBROUTINE
'''

