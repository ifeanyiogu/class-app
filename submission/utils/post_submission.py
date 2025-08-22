from assignment.models import Assignment
from rest_framework import status
from class_session.utils import verify_membership
from django.utils import timezone
from submission.models import Submission


def post(request, pk):
    user = request.user
    try:
        assignment = Assignment.objects.get(pk=pk)
    except Assignment.DoesNotExist:
        return {
            'error':'assignment not available',
            'status':status.HTTP_404_NOT_FOUND
        }
    verified = verify_membership.verify(user, assignment.session.classroom)
    if verified.get('error') is not None:
        return verified
    if not assignment.is_published:
        return {
            'error':'assignment not published yet',
            'status':status.HTTP_400_BAD_REQUEST
        }
    if assignment.deadline <= timezone.now():
       return {
           'error':'deadline is reached',
           'status':status.HTTP_400_BAD_REQUEST
       }
    
    payload = request.data
    note = payload.get('note')
    if note is None or note.strip() == '':
       return {
           'error':'No note provided',
           'status':status.HTTP_400_BAD_REQUEST
       }
    _note = note.strip()
    try:
       new_sub = Submission.objects.create(user=user, session=assignment.session, assignment=assignment, note=_note)
    except Exception as e:
       print(str(e))
       return {
           'error':'something went wrong, try again',
           'status':status.HTTP_400_BAD_REQUEST
       }
    return {
        'id':new_sub.pk,
        'note':new_sub.note,
        'status':status.HTTP_201_CREATED
    } 