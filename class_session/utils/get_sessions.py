from classroom.models import ClassRoom, ClassMember
from class_session.models import ClassSession, Lecture
from rest_framework import status

def get(request, classroom):
    user = request.user
    if not user.is_authenticated:
        return {
            'error': 'you are not logged in',
            'status':status.HTTP_401_UNAUTHORIZED
        }
    try:
        class_room = ClassRoom.objects.get(room_id=classroom)
    except ClassRoom.DoesNotExist:
        return {
            'error': 'classroom with class Id does not exist',
            'status':status.HTTP_404_NOT_FOUND
        }
    try:
        member = ClassMember.objects.get(user=user, classroom=class_room, is_approved=True)
    except ClassMember.DoesNotExist:
        return {
            'error': 'You Are Not A Member',
            'status':status.HTTP_401_UNAUTHORIZED
        }
    sessions = ClassSession.objects.filter(classroom=class_room, is_published=True).select_related('lecture').order_by('-date')
    
    data = [
        {
            "id":ses.pk,
            "date":ses.date,
            "topic":ses.lecture.topic
        }
        for ses in sessions
    ]
    return {
        "data":data,
        "status":status.HTTP_200_OK
    }
    