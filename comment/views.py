from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import all_comments, create_comments, one_comment, create_reply, all_replies

# Create your views here.
class AllComments(APIView):
   def get(self, request, pk):
       data = all_comments.get(request, pk)
       return Response(data, status=data['status'])
       
       
class AllReplies(APIView):
   def get(self, request, pk):
       data = all_replies.get(request, pk)
       return Response(data, status=data['status'])
       

class CreateComment(APIView):
   def post(self, request, pk):
       data = create_comments.post(request, pk)
       return Response(data, status=data['status'])


class OneComment(APIView):
   def get(self, request, pk):
       data = one_comment.get(request, pk)
       return Response(data, status=data['status'])
       
       
class CreateReply(APIView):
   def post(self, request, pk):
       data = create_reply.post(request, pk)
       return Response(data, status=data['status'])