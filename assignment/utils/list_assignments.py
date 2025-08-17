from class_session.utils import verify_membership
from class_session.models import ClassSession 
from rest_framework import status
from django.utils import timezone


def get(request, pk):
    user = request.user
    try:
        session = ClassSession.objects.prefetch_related('assignments').get(pk=pk)
    except ClassSession.DoesNotExist:
        return {
            'error':'Session id is invalid',
            'status':status.HTTP_404_NOT_FOUND
        }
    verified = verify_membership.verify(user, session.classroom)
    if verified.get('error'):
        return verified
    member = verified['member']
    data = [
        {
            'id':asign.pk,
            'note':asign.note,
            'deadline':asign.deadline
        }
        for asign in session.assignments.filter(is_published=True, deadline__gte=timezone.now())
    ]
    return {
        'data':data,
        'status':status.HTTP_200_OK
    }