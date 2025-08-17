from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import list_assignments, one_assignment, create_assignment
from rest_framework.parsers import MultiPartParser

# Create your views here.
class ListAssignments(APIView):
    def get(self, request, pk):
        data = list_assignments.get(request, pk)
        return Response(data, status=data['status'])
        
class OneAssignment(APIView):
    def get(self, request, pk):
        data = one_assignment.get(request, pk)
        print(f"this data status is {data.get('status')}")
        return Response(data, status=data['status'])
        

class CreateAssignment(APIView):
    parser_classes = [MultiPartParser]
    def post(self, request, pk):
        data = create_assignment.post(request, pk)
        return Response(data, status=data['status'])