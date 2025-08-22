from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import one_submission, all_submission, post_submission, mark_submission

# Create your views here.

class OneSubmission(APIView):
    def get(self, request, pk):
        data = one_submission.get(request, pk)
        return Response(data, status=data['status'])
        
class AllSubmission(APIView):
    def get(self, request, pk):
        data = all_submission.get(request, pk)
        return Response(data, status=data['status'])
        

class PostSubmission(APIView):
    def post(self, request, pk):
        data = mark_submission.post(request, pk)
        return Response(data, status=data['status'])
        
        
class MarkSubmission(APIView):
    def post(self, request, pk):
        data = mark_submission.post(request, pk)
        return Response(data, status=data['status'])