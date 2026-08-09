from rest_framework import generics, viewsets
from .models import Application
from .serializers import ApplicationSerializer
from rest_framework.permissions import IsAuthenticated
from jobs.permissions import *



class ApplicationListAPIView(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ApplicationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsApplicationOwner]


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated, IsSeeker]

        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsAuthenticated, IsApplicationEmployer]

        else:
            permission_classes = [IsAuthenticated, IsApplicationOwner]

        return [permission() for permission in permission_classes]