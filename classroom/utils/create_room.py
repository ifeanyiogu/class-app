from classroom.models import ClassRoom
from django.conf import settings
from rest_framework import status
import random

def post(request):
  user = request.user
  if not user.is_authenticated:
    return {
      'error': 'Login before continuing',
      'status': status.HTTP_401_UNAUTHORIZED
    }
  if not user.is_verified:
    return {
      'error':'verify your profile',
      'status': status.HTTP_401_UNAUTHORIZED
    }
  
  data = request.data
  room_name = data.get('name')
  
  if not room_name or room_name.strip() == '':
    return {
      'error': 'invalid room name',
      'status': status.HTTP_400_BAD_REQUEST
    }
  room = room_name.strip()
  if ClassRoom.objects.filter(name=room).exists():
    return {
      'error':'Class room with name already exist',
      'status': status.HTTP_400_BAD_REQUEST
      
    }
  
      
  new_room = ClassRoom.objects.create(
    name=room,
    creator=user
  )
  return {
    'name': new_room.name,
    'url': f'{settings.FRONT_END_URL}/class/{new_room.room_id}/',
    'status': status.HTTP_200_OK
  }
  
  
  
  