from rest_framework import status
from comment.models import Comment, Reply
from class_session.models import ClassSession
from class_session.utils import verify_membership
from .all_comments import get_user


def post(request, pk):
    user = request.user
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return {
            'error':'comment is not available',
            'status':status.HTTP_404_NOT_FOUND
        }
    verified = verify_membership.verify(user, comment.session.classroom)
    if verified.get('error') is not None:
        return verified
    payload = request.data
    if not payload.get('note') or not payload.get('note').strip():
        return {
            'error':'no reply provided',
            'status':status.HTTP_400_BAD_REQUEST
        }
    note = payload.get('note').strip()
    
    new_com = Reply.objects.create(user=user, session=comment.session, note=note, comment=comment)
    
    return {
            'id':new_com.pk,
            'user':get_user(new_com, user),
            'note':new_com.note,
            'status':status.HTTP_201_CREATED
        }