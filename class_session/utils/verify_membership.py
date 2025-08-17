from class_session.models import ClassSession
from classroom.models import ClassMember
from rest_framework import status

def verify(user, class_room):
    if not user.is_authenticated:
        print('f1')
        return {
            'error': 'you are not logged in',
            'status':status.HTTP_401_UNAUTHORIZED
        }
    
    try:
        member = ClassMember.objects.get(user=user, classroom=class_room, is_approved=True)
    except ClassMember.DoesNotExist:
        print('f2')
        return {
            'error': 'You Are Not A Member',
            'status':status.HTTP_401_UNAUTHORIZED
        }
    return {'member':member}