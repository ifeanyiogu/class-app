from classroom.models import ClassRoom, ClassMember
from rest_framework import status

def post(request, id):
 user = requeat.user
 if not user.is_authenticated:
   return {
     "error": "Login before proceeding",
     "status": status.HTTP_401_UNAUTHORIZED
   }
 try:
   room = ClassRoom.objects.get(room_id=id)
 except ClassRoom.DoesNotExist:
   return {
     "error": f"Classroom with id {id} not found",
     "status": status.HTTP_404_NOT_FOUND
   }
 try:
    membership = ClassMember.objects.get(user=user, classroom=room)
    membership.delete()
    return {
      "message": "You Are No Longer a Member",
      "status": status.HTTP_200_OK
    }
 except ClassMember.DoesNotExist:
    return {
      "error": "You Are Not A Member of This Classroom",
      "status": status.HTTP_401_UNAUTHORIZED
    }
    