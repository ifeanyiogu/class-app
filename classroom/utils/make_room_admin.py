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
 if not room.creator == user:
    return {
      "error": "Only The Creator Can Select An Admin",
      "status": status.HTTP_401_UNAUTHORIZED
    }
 if ClassMember.objects.filter(role="admin").exists():
    return {
      "error": "Admin Already Exist",
      "status": status.HTTP_400_BAD_REQUEST
    }
 memembership.role = "admin"
 memembership.save(update_fields=["role"])
 return {
      "membership_id": membership.pk,
      "role":membership.get_role_display(),
      "status": status.HTTP_200_OK
    }
    