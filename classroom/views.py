from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .utils import get_room, create_room,\
room_description, room_join,\
room_leave, make_room_admin,\
approve_member, remove_admin
# Create your views here.


class HomeClassRoom(APIView):
  def get(self, request):
    query = request.query_params.get("id")
    data = get_room.get(query)
    if data.get('error'):
      return Response(data, status=status.HTTP_400_BAD_REQUEST)
    return Response(data, status=status.HTTP_200_OK)
    
  def post(self, request):
    data = create_room.post(request)
    return Response(data, status = data['status'])
    

class ClassRoomView(APIView):
  def get(self, request, id):
    data = room_description.get(request, id)
    return Response(data, status=data["status"])
    
    
class JoinClassRoom(APIView):
  def post(self, request, id):
    data = room_join.post(request, id)
    return Response(data, status=data["status"])
    
    
class LeaveClassRoom(APIView):
  def post(self, request, id):
    data = room_leave.post(request, id)
    return Response(data, status=data["status"])
    
    
class AdminClassRoom(APIView):
  def post(self, request, id, pk):
    data = make_room_admin.post(request, id, pk)
    return Response(data, status=data["status"])


class MemberApproveView(APIView):
  def post(self, request, id, pk):
    data = approve_member.post(request, id, pk)
    return Response(data, status=data["status"])
    
    
class AdminRemoveView(APIView):
  def post(self, request, id, pk):
    data = remove_admin.post(request, id, pk)
    return Response(data, status=data["status"])