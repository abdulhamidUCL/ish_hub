from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .decorators import *
from .forms import *
from .models import *
from django.shortcuts import get_object_or_404


# Create your views here.

@login_required
@employer_required
def company_create(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)

        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.save()
            return redirect('home')
    else:
        form = CompanyForm()

    return render(request, 'companies/company_create.html', {'form': form})


@login_required
@employer_required
def company_edit(request):
    company = Company.objects.filter(owner=request.user).first()

    if not company:
        return redirect('company_create')

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CompanyForm(instance=company)

    return render(request, 'companies/company_edit.html', {'form': form})


@login_required
@employer_required
def company_detail(request):
    company = Company.objects.filter(owner=request.user).first()

    if company is None:
        return redirect("company_create")

    return render(request, 'companies/company_detail.html', {'company': company})