from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count
from .models import *
from applications.models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.decorators import employer_required


import json
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views import View
from applications.models import Application


# Create your views here.
@login_required
def job_search(request):
    q = request.GET.get("q", "").strip()
    city = request.GET.get("city", "").strip()

    jobs = Job.objects.filter(is_active=True)

    if q:
        jobs = jobs.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(company__icontains=q) |
            Q(city__icontains=q)
        )

    if city:
        jobs = jobs.filter(city__icontains=city)

    jobs = jobs.order_by("-created_at")

    return render(request, "jobs/job_search.html", {
        "jobs": jobs,
        "q": q,
        "city": city,
    })

@login_required
@employer_required
def create_job(request):
    if not hasattr(request.user, "company"):
        return redirect("company_create")
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user.company
            if not job.company:
                return redirect('company_create')
            form.save()
            return redirect('my_jobs')
    else:
        form = JobForm()

    return render(request, 'jobs/create_job.html', {'form': form})

@login_required
@employer_required
def view_job(request, job_id):
    job = get_object_or_404(Job,company__owner=request.user, pk=job_id, company=request.user.company)

    if not hasattr(request.user, "company"):
        return HttpResponseForbidden()

    return render(request, 'jobs/view_job.html', {'job': job})


@login_required
@employer_required
def job_list(request):
    jobs = Job.objects.filter(company__owner=request.user)



    return render(request, 'jobs/job_list.html', {'jobs': jobs})


@login_required
@employer_required
def edit_job(request, job_id):
    job = get_object_or_404(Job,company__owner=request.user ,pk=job_id, company=request.user.company)

    if not hasattr(request.user, "company"):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('my_jobs')
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/edit_job.html', {'form': form})

@login_required
@employer_required
def delete_job(request, job_id):
    job = get_object_or_404(Job,company__owner=request.user ,pk=job_id, company=request.user.company)

    if not hasattr(request.user, "company"):
        return HttpResponseForbidden()

    if request.method == 'POST':
        job.delete()
        return redirect('my_jobs')
    return render(request, 'jobs/delete_job.html', {'job': job})

@method_decorator(login_required, name='dispatch')
@method_decorator(employer_required, name='dispatch')
class UpdateApplicationStatus(View):
    def post(self, request, application_id):
        application = get_object_or_404(Application, id=application_id)

        if application.job.company.owner != request.user:
            return JsonResponse({'error': 'You do not own this job listing.'}, status=403)

        try:
            data = json.loads(request.body)
            new_status = data.get('status')

            if new_status in dict(Application.STATUS_CHOICES):
                application.status = new_status
                application.save()
                return JsonResponse({'message': f'Status updated to {new_status}'}, status=200)

            return JsonResponse({'error': 'Invalid status choice.'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)


@login_required
@employer_required
def my_jobs(request):
    jobs = (
        Job.objects.filter(company__owner=request.user)
        .select_related("company")
        .annotate(
            applicant_count=Count("application"),
            pending_count=Count(
                "application",
                filter=Q(application__status="pending")
            ),
            accepted_count=Count(
                "application",
                filter=Q(application__status="accepted")
            ),
            rejected_count=Count(
                "application",
                filter=Q(application__status="rejected")
            ),
        )
        .order_by("-created_at")
    )

    sort = request.GET.get("sort")

    if sort == "new":
        jobs = jobs.order_by("-created_at")
    elif sort == "old":
        jobs = jobs.order_by("created_at")
    elif sort == "a-z":
        jobs = jobs.order_by("title")
    elif sort == "z-a":
        jobs = jobs.order_by("-title")

    return render(request, "jobs/my_jobs.html", {"jobs": jobs})


@login_required
@employer_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id, company__owner=request.user, company=request.user.company)

    if not hasattr(request.user, "company"):
        return HttpResponseForbidden()

    pending_count = Application.objects.filter(job=job, status="pending",).count()

    accepted_count = Application.objects.filter(job=job,status="accepted",).count()

    rejected_count = Application.objects.filter(job=job, status="rejected",).count()

    context = {
        "job": job,
        "pending_count": pending_count,
        "accepted_count": accepted_count,
        "rejected_count": rejected_count,
    }

    return render(request,"jobs/job_detail.html", context,)


