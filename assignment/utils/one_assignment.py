from assignment.models import Assignment
from rest_framework import status
from class_session.utils import verify_membership
from django.conf import settings

def get_image_url(obj):
    try:
        if settings.DEBUG:
            print(f"{settings.HOST_URL}{obj.audio.url}")
            return f"{settings.HOST_URL}{obj.audio.url}"
        else:
            return ""
    except:
        return ''
        
        
def get(request, pk):
    user = request.user
    try:
        assignment = Assignment.objects.get(pk=pk)
    except Assignment.DoesNotExist:
        return {
            'error':'Assignment does not exist',
            'status':status.HTTP_404_NOT_FOUND
        }
    class_room = assignment.session.classroom
    verified = verify_membership.verify(user, class_room)
    if verified.get('error'):
        return verified
    return {
        'id':assignment.pk,
        'note':assignment.note,
        'status':status.HTTP_200_OK,
        'audio':get_image_url(assignment)
    }