from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from .utils import get_sessions, one_session, one_session_files, update_lecture, create_session



# Create your views here.
class AllSessionsView(APIView):
   
    def get(self, request, classroom):
        data = get_sessions.get(request, classroom)
        return Response(data, status=data['status'])
        
        

class OneSessionView(APIView):
    def get(self, request, pk):
        data = one_session.get(request, pk)
        return Response(data, status=data["status"])
        
        
class OneSessionFilesView(APIView):
    def get(self, request, pk):
        data = one_session_files.get(request, pk)
        return Response(data, status=data["status"])
        
        
class UpdateLectureView(APIView):
    parser_classes = [MultiPartParser]
    def post(self, request, pk):
        data = update_lecture.post(request, pk)
        return Response(data, status=data["status"])
        

class CreateSessionView(APIView):
    parser_classes = [MultiPartParser]
    def post(self, request, classroom):
        data = create_session.post(request, classroom)
        return Response(data, status=data['status'])
        