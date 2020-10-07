from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, CustomPasswordUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views, update_session_auth_hash

def register(request):
    if request.user.is_authenticated:#redirects logged in users
       return redirect('teacher-portal')
    else:
        if request.method=='POST':
            #username = email and is all lowercase
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username=form.cleaned_data.get('username')
                messages.success(request, f'Account created for { username }, please login!')
                return redirect('login')
        else:
            form = UserRegisterForm()
        return render(request, 'teachers/register.html', {'form':form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomPasswordUpdateForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated!')
            return redirect('login')
        else:
            messages.error(request, 'Error')
    else:
        form = CustomPasswordUpdateForm(request.user)
    return render(request, 'teachers/profile.html', {
        'form': form
    })


