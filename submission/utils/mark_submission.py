from submission.models import Submission
from rest_framework import status
from class_session.utils import verify_admin

def post(request, pk):
    user = request.user
    try:
        submission = Submission.objects.get(pk=pk)
    except Submission.DoesNotExist:
        return {
            'error':'Submission not available',
            'status':status.HTTP_404_NOT_FOUND
        }
    verified = verify_admin.verify(user, submission.session.classroom)
    if verified.get('error'):
        return verified
    payload = request.data
    score = payload.get('score')
    if score is None or score.strip() =='':
        return {
            'error':'No score provided',
            'status':status.HTTP_400_BAD_REQUEST
        }
    remarks = {
        'FAIL':0,
        'PASS': 2,
        'GOOD':4,
        'EXCELLENT':5
    }
    remark = score.strip().upper()
    if not remark in remarks:
        return {
            'error':'invalid remark',
            'status':status.HTTP_400_BAD_REQUEST
        }
    if submission.marked:
        return {
            'error':'submission already marked',
            'status':status.HTTP_400_BAD_REQUEST
        }
    submission.marked = True
    submission.score = remarks[remark]
    submission.save()
    return {
        'id':submission.pk,
        'score':submission.score,
        'marked':str(submission.marked).lower(),
        'status':status.HTTP_200_OK
    }