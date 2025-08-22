from rest_framework import status
from comment.models import Comment
from class_session.models import ClassSession
from class_session.utils import verify_membership


def get_user(obj, user):
    if obj.user == user:
        return "YOU"
    if obj.user.is_verified:
        return f'{obj.user.last_name} {obj.user.first_name}'
    else:
        return obj.user.username

def get(request, pk):
    user = request.user
    try:
        session = ClassSession.objects.prefetch_related('comments').get(pk=pk)
    except ClassSession.DoesNotExist:
        return {
            'error':'session is not available',
            'status':status.HTTP_404_NOT_FOUND
        }
    verified = verify_membership.verify(user, session.classroom)
    if verified.get('error') is not None:
        return verified
    comments = session.comments.all().order_by('-date')
    data = [
        {
            'id':com.pk,
            'user':get_user(com, user),
            'note':com.note,
        }
        for com in comments
    ]
    return {
        'data':data,
        'status':status.HTTP_200_OK
    }