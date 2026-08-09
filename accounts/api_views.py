from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Resume
from .serializers import ResumeSerializer
from jobs.permissions import *



class ResumeListAPIView(generics.ListCreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ResumeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated, IsOwner]





class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated, IsSeeker]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)