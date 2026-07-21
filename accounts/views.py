from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import Profile, Resume
from .decorators import *
# Create your views here.

def home(request):
    return render(request, 'accounts/main.html')

def register(request):
    if request.method == "POST":
        form = RegisterForm(data=request.POST)

        if form.is_valid():
            user = form.save(commit=True)
            Profile.objects.create(
                user=user,
                role=form.cleaned_data['role']
            )

            return redirect('user_login')

        messages.error(request, 'Register failed')

    else:
        form = RegisterForm()
    context = {
        'form': form,
        'title': 'Registration'
    }
    return render(request, 'accounts/components/register.html', context)


def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                # messages.success(request, 'Welcome!')
                return redirect('home')
        messages.error(request, 'Login failed')
        return redirect('user_login')
    else:
        form = LoginForm()
    context = {
        'form': form,
        'title': 'Authentication'
    }
    return render(request, 'accounts/components/login.html', context)

def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )
        if form.is_valid():
            form.save()
            return redirect("view_profile", pk=request.user.pk)
        print(form.errors)

    else:
        form = ProfileForm(instance=profile)

    return render(request,"accounts/components/edit_profile.html",{"form": form})

@login_required
def view_profile(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        messages.error(request, "That user does not exist.")
        return redirect("home")

    profile, created = Profile.objects.get_or_create(user=user)
    resume = getattr(user, "resume", None)


    if profile.user != request.user:
        return HttpResponseForbidden("You don't have permission.")

    return render(request, "accounts/components/view_profile.html", {"profile": profile, "resume": resume,})

@login_required
@seeker_required
def edit_resume(request):
    resume, created = Resume.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ResumeForm(instance=resume, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")

    else:
        form = ResumeForm(instance=resume)

    return render(request, "accounts/components/edit_resume.html", {"form": form})

