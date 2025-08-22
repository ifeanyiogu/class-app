from submission.models import Submission
from rest_framework import status
from class_session.utils import verify_membership

def get(request, pk):
    user = request.user
    try:
        submission = Submission.objects.get(pk=pk)
    except Submission.DoesNotExist:
        return {
            'error':'submission object does not exist',
            'status':status.HTTP_404_NOT_FOUND
        }
    verified = verify_membership.verify(user, submission.session.classroom)
    if verified.get('error') is not None:
        return verified
    if not submission.user == user:
        return {
            'error':'only the owner can view this',
            'status':status.HTTP_401_UNAUTHORIZED
        }
    data = {
        'id':submission.pk,
        'assignment':{
            'id':submission.assignment.pk,
            'note':submission.assignment.note
        },
        'note':submission.note,
        'marked':str(submission.marked).lower(),
        'score':submission.score,
        'user':submission.user.username,
        'status':status.HTTP_200_OK
    }
    return data
    