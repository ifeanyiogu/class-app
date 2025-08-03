from classroom.models import ClassRoom, ClassMember
from rest_framework import status

def post(request, id, pk):
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
    membership = ClassMember.objects.get(pk=pk)
 except ClassMember.DoesNotExist:
    return {
      "error": "Member Does Not Exist",
      "status": status.HTTP_404_NOT_FOUND
    }
 if not room.creator == user or not ClassMember.objects.filter(user=user, is_approved=True, is_admin=True, classroom=room).exists():
    return {
      "error": "Only The Creator Or Admin Can Approve A Member",
      "status": status.HTTP_401_UNAUTHORIZED
    }
 memembership.is_approved = True
 memembership.save(update_fields=["is_approved"])
 return {
      "membership_id": membership.pk,
      "is_approved": membership.is_approved,
      "status": status.HTTP_200_OK
    }
    