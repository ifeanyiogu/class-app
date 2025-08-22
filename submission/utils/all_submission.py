from class_session.models import ClassSession
from rest_framework import status
from class_session.utils import verify_membership
from django.db.models import Prefetch

def get(request, pk):
    user = request.user
    try:
        session = ClassSession.objects.get(pk=pk)
    except ClassSession.DoesNotExist:
        return {
            'error':'session Not Found',
            'status':status.HTTP_404_NOT_FOUND
        }
    verified = verify_membership.verify(user, session.classroom)
    if verified.get('error') is not None:
        return verified
    data = [
        {
            'id':submis.pk,
            'assignment':{
                'id':submis.assignment.pk,
                'note':submis.assignment.note
            },
            'note':submis.note,
            'marked':str(submis.marked).lower()
        }
        for submis in session.submissions.filter(user=user).select_related('assignment').order_by('-date')
    ]
    return {
        'data':data,
        'status':status.HTTP_200_OK
    }
    