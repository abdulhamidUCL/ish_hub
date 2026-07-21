from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from accounts.decorators import seeker_required, employer_required
from accounts.models import Resume
from jobs.models import Job
from applications.models import Application


@login_required
def dashboard_redirect(request):
    profile = getattr(request.user, 'profile', None)

    if profile is None:
        return redirect('home')

    if profile.role == 'seeker':
        return redirect('seeker_dashboard')
    elif profile.role == 'employer':
        return redirect('employer_dashboard')

    return redirect('home')


@login_required
@seeker_required
def seeker_dashboard(request):
    recent_applications = (
        Application.objects.filter(user=request.user)
        .select_related('job', 'job__company')
        .order_by('-applied_at')[:5]
    )

    try:
        resume = request.user.resume
    except Resume.DoesNotExist:
        resume = None

    # "complete" = every field a seeker would want an employer to see is filled in
    resume_complete = bool(
        resume
        and resume.title
        and resume.skills
        and resume.experience
        and resume.education
        and resume.resume_file
    )

    open_jobs_count = Job.objects.filter(is_active=True).count()

    context = {
        'recent_applications': recent_applications,
        'resume': resume,
        'resume_complete': resume_complete,
        'open_jobs_count': open_jobs_count,
    }
    return render(request, 'dashboard/seeker_dashboard.html', context)


@login_required
@employer_required
def employer_dashboard(request):
    company = getattr(request.user, 'company', None)

    if company is None:
        return redirect('company_create')

    active_jobs_count = Job.objects.filter(company=company, is_active=True).count()
    total_applicants = Application.objects.filter(job__company=company).count()
    recent_applications = (
        Application.objects.filter(job__company=company)
        .select_related('job', 'user')
        .order_by('-applied_at')[:5]
    )

    context = {
        'company': company,
        'active_jobs_count': active_jobs_count,
        'total_applicants': total_applicants,
        'recent_applications': recent_applications,
    }
    return render(request, 'dashboard/employer_dashboard.html', context)
