from attendance.models import Attendance
from class_session.models import ClassSession
from classroom.models import ClassMember
from rest_framework import status

def post(request, pk):
    user = request.user
    if not user.is_authenticated:
        return {
            'error':'You Are Not Logged In',
            'status':status.HTTP_401_UNAUTHORIZED
        }
    try:
        session = ClassSession.objects.get(pk=pk, is_published=True)
    except ClassSession.DoesNotExist:
        return {
            'error':'session does not exist or is not published yet',
            'status':status.HTTP_404_NOT_FOUND
        }
    try:
        member = ClassMember.objects.get(classroom=session.classroom, user=user, is_approved=True)
    except ClassMember.DoesNotExist:
        return {
            'error':'You Are Not Yet A Member',
            'status':status.HTTP_401_UNAUTHORIZED
        }
    if session.is_expired:
        return {
            'error':'Session is over',
            'status':status.HTTP_400_BAD_REQUEST
        }
    if Attendance.objects.filter(user=user, session=session).exists():
        return {
            'error':'You have done that already',
            'status':status.HTTP_400_BAD_REQUEST
        }
    _attendance = Attendance.objects.create(user=user, session=session)
    return {
        'message':'attended',
        'status':status.HTTP_201_CREATED
    }