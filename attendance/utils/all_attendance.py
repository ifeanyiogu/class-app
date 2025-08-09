from attendance.models import Attendance
from class_session.models import ClassSession
from classroom.models import ClassMember
from rest_framework import status

def show_info(name):
    if (name.first_name and name.first_name.strip() != ""):
        if name.last_name and name.last_name.strip() != "":
            return f"{name.first_name} {name.last_name}"
        else:
            return f"{name.first_name}"
    else:
        return name.username
    
        

def get(request, pk):
    user = request.user
    if not user.is_authenticated:
        return {
            'error':'You Are Not Logged In',
            'status':status.HTTP_401_UNAUTHORIZED
        }
    try:
        session = ClassSession.objects.prefetch_related('session_attendance').get(pk=pk, is_published=True)
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
    all_attended = session.session_attendance.select_related('user').all().order_by('date')
    data = [
        show_info(name.user)
        for name in all_attended
    ]
    return {
        'data':data,
        'status':status.HTTP_200_OK
    }