from rest_framework import status
from comment.models import Comment
from class_session.models import ClassSession
from class_session.utils import verify_membership
from .all_comments import get_user


def get(request, pk):
    user = request.user
    try:
        comment = Comment.objects.prefetch_related('replies').get(pk=pk)
    except Comment.DoesNotExist:
        return {
            'error':'comment is not available',
            'status':status.HTTP_404_NOT_FOUND
        }
    verified = verify_membership.verify(user, comment.session.classroom)
    if verified.get('error') is not None:
        return verified
    replies = comment.replies.all().order_by('-date')
    data = [
        {
            'id':com.pk,
            'user':get_user(com, user),
            'note':com.note,
        }
        for com in replies
    ]
    return {
        'data':data,
        'status':status.HTTP_200_OK
    }