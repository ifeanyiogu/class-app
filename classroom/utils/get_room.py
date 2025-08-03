from classroom.models import ClassRoom
from django.conf import settings

def get(id):
  if not id or id.strip() == '':
    return {
      'error':'invalid id'
    }
  
  try:
    class_room = ClassRoom.objects.get(room_id=id)
  except ClassRoom.DoesNotExist:
    return {
      'error':f'classroom with id {id} not found'
    }
  return {
    'name': class_room.name,
    'creator': f"{class_room.creator.first_name} {class_room.creator.last_name}",
    'url': f'{settings.FRONT_END_URL}/class/{class_room.room_id}/'
  }