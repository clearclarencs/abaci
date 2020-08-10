from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

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
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Account updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {
        'u_form': u_form
    }
    return render(request, 'teachers/profile.html', context)

