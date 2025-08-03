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
 if not user.is_verified:
    return {
      "error": "verify your account",
      "status": status.HTTP_401_UNAUTHORIZED
    }
 try:
    membership = ClassMember.objects.get(user=user, classroom=room)
    if membership.is_approved:
      return {
        "error": "you are already a member",
        "status":status.HTTP_401_UNAUTHORIZED
      }
    else:
      return {
        "error":"Your previous request is still awaiting approval",
        "status": status.HTTP_401_UNAUTHORIZED
      }
 except ClassMember.DoesNotExist:
    new_membership = ClassMember.objects.create(user=user,classroom=room)
    return {
      "message": "Join Request Sent",
      "membership_id": new_membership.pk,
      "status": status.HTTP_201_CREATED
    }
    