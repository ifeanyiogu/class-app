from classroom.models import ClassRoom, ClassMember
from django.db.models import Prefetch
from rest_framework import status

def get_admin(admin):
  if not admin:
    return None
  else:
    return f"{admin.first_name} {admin.last_name}"

def get(request, id):
  user = request.user
  try:
   class_room = ClassRoom.objects.prefetch_related(
     Prefetch(
       "members",
       queryset=ClassMember.objects.filter(is_approved=True).select_related("user")
     )
   ).get(room_id=id)
  except ClassRoom.DoesNotExist:
   return {
     'error':'room id not found',
     'status': status.HTTP_404_NOT_FOUND
   }
  members = class_room.members.count()
  admin = None
  membership = False
  recently_joined = []
  try:
   member_admin = class_room.members.filter(role="admin").first()
   admin = member_admin.user
  except:
   pass
  if (user.is_authenticated and class_room.members.filter(user=user, is_approved=True).exists()) or (user.is_authenticated and class_room.creator == user):
   membership = True
  recently_joined = class_room.members.filter(is_approved=True).order_by("-date")[:5]
 
  data = {
   "name":class_room.name,
   "creator":f"{class_room.creator.first_name} {class_room.creator.last_name}",
   "date": class_room.date,
   "admin":get_admin(admin),
   "membership":membership,
   "recently_joined": [
     f"{member.user.first_name} {member.user.last_name}"
     for member in recently_joined
   ],
   "status": status.HTTP_200_OK
  }
  return data
 