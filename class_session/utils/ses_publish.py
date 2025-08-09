from class_session.models import ClassSession, Lecture
from classroom.models import ClassMember, ClassRoom
from rest_framework import status
from django.core.exceptions import ValidationError
def show_error(e):
    if hasattr(e,"message"):
        return e.message
    elif hasattr(e, "messages"):
        return "; ".join(e.messages)
    elif hasattr(e, "message_dict"):
        return e.message_dict
    else:
        return "unexpected error"

def post(request, class_r):
    user = request.user
    if not user.is_authenticated:
        return {
            'error': 'you are not logged in',
            'status':status.HTTP_401_UNAUTHORIZED
        }
    try:
        session = ClassSession.objects.get(pk=class_r)
    except ClassSession.DoesNotExist:
        return {
            'error': 'class session id is invalid',
            'status':status.HTTP_404_NOT_FOUND
        }
    try:
        member = ClassMember.objects.get(user=user, classroom=session.classroom, is_approved=True)
    except ClassMember.DoesNotExist:
        return {
            'error': 'You Are Not A Member',
            'status':status.HTTP_401_UNAUTHORIZED
        }
    if not member.role == 'admin' and not session.classroom.creator == user:
        return {
            'error': 'only the admin and class creator can create a session',
            'status':status.HTTP_401_UNAUTHORIZED
        }
    if session.is_published:
        return {
            'error': 'session is already published',
            'status':status.HTTP_400_BAD_REQUEST
        }
    session.is_published = True
    session.save()
    return {
        'message':'published',
        'status':status.HTTP_201_CREATED
    }
    

    