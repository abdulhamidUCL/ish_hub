from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from .forms import *
from accounts.decorators import seeker_required
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from accounts.decorators import employer_required
from django.views.decorators.http import require_POST


# Create your views here.

@login_required
@seeker_required
def job_apply(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    #if already applied
    already_applied = Application.objects.filter(job=job, user=request.user).exists()
    if already_applied:
        messages.error(request, "You already applied for this job")
        return redirect('my_applications')

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.user = request.user
            application.save()
            messages.success(request, "Application submitted")
            return redirect('my_applications')

    else:
        form = ApplicationForm()

    return render(request, 'applications/job_apply.html', {'form': form, 'job': job})

@login_required
@seeker_required
def my_applications(request):
    application = Application.objects.filter(user=request.user).order_by('-applied_at')

    return render(request, 'applications/my_applications.html', {'application': application})


@login_required
@employer_required
def all_applications(request):
    if not hasattr(request.user, "company"):
        return redirect("company_create")

    application = Application.objects.filter(
        job__company__owner=request.user
    ).select_related('job', 'user').order_by('-applied_at')

    return render(request, 'applications/all_applications.html', {'application': application})


@login_required
@employer_required
def applicant_list(request, job_id):

    job = get_object_or_404(Job, id=job_id, company__owner=request.user)

    applications = (Application.objects.filter(job=job).select_related(
            "user",
            "user__profile",
            "user__resume",
        ).order_by("-applied_at"))

    return render(request,"applications/applicant_list.html",
        {
            "job": job,
            "applications": applications
        }
    )


@login_required
@employer_required
def applicant_detail(request, application_id):

    application = get_object_or_404(Application.objects.select_related(
            "user",
            "user__profile",
            "user__resume",
            "job",
            "job__company",
        ),
        id=application_id,
        job__company__owner=request.user
    )

    return render(request,"applications/applicant_detail.html",
        {
            "application": application,
            "profile": application.user.profile,
            "resume": getattr(application.user, "resume", None),
        },
    )


@login_required
@employer_required
@require_POST
def accept_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, job__company__owner=request.user,)

    application.status = "accepted"
    application.save(update_fields=["status"])

    messages.success(request, "Application accepted.")

    return redirect("applicant_detail", application.id)

@login_required
@employer_required
@require_POST
def reject_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, job__company__owner=request.user,)

    application.status = "rejected"
    application.save(update_fields=["status"])

    messages.success(request, "Application rejected.")

    return redirect("applicant_detail", application_id=application.id)


