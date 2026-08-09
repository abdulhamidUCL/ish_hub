from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import *
from rest_framework import viewsets


class JobListAPIView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get(self, request):
        jobs = self.get_queryset()

        city = request.query_params.get("city")
        employment_type = request.query_params.get("employment_type")
        search = request.query_params.get("search")

        if city:
            jobs = jobs.filter(city__iexact=city)

        if employment_type:
            jobs = jobs.filter(employment_type=employment_type)

        if search:
            jobs = jobs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(requirements__icontains=search) |
                Q(city__icontains=search) |
                Q(category__icontains=search)
            )


        ordering = request.query_params.get("ordering")

        if ordering:
            jobs = jobs.order_by(ordering)

        page = self.paginate_queryset(jobs)

        if page is not None:
            serializer = JobSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)


class JobDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]




class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer, IsJobOwner]

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated, IsEmployer]

        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [
                IsAuthenticated,
                IsEmployer,
                IsJobOwner,
            ]

        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        jobs = Job.objects.all()

        city = self.request.query_params.get("city")
        employment_type = self.request.query_params.get("employment_type")
        search = self.request.query_params.get("search")
        ordering = self.request.query_params.get("ordering")

        if city:
            jobs = jobs.filter(city__iexact=city)

        if employment_type:
            jobs = jobs.filter(employment_type=employment_type)

        if search:
            jobs = jobs.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(requirements__icontains=search)
                | Q(city__icontains=search)
                | Q(category__icontains=search)
            )

        if ordering:
            jobs = jobs.order_by(ordering)

        return jobs

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)
