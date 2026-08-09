from rest_framework import generics, viewsets
from .models import Company
from .serializers import CompanySerializer
from rest_framework.permissions import IsAuthenticated
from jobs.permissions import *


class CompanyListAPIView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CompanyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsCompanyOwner, IsAuthenticated]


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated]

        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [
                IsAuthenticated,
                IsCompanyOwner,
            ]

        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)