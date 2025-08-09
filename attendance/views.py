from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import all_attendance, attend
# Create your views here.

class AllAttendance(APIView):
    def get(self, request, pk):
        data = all_attendance.get(request, pk)
        return Response(data, status=data['status'])
        

class AttendSession(APIView):
    def post(self, request, pk):
        data = attend.post(request, pk)
        return Response(data, status=data['status'])