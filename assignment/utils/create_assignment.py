from class_session.models import ClassSession
from rest_framework import status
from class_session.utils import verify_admin, audio_c
from assignment.models import Assignment
from django.conf import settings

def get_image_url(obj):
    try:
        if settings.DEBUG:
            return f"{settings.HOST_URL}{obj.audio.url}"
        else:
            return ""
    except:
        return ''

def post(request, pk):
    data = request.data
    user = request.user
    try:
        session = ClassSession.objects.get(pk=pk)
    except ClassSession.DoesNotExist:
        return {
            'error':'session id invalid',
            'status':status.HTTP_404_NOT_FOUND
        }
    verified = verify_admin.verify(user, session.classroom)
    if verified.get('error') is not None:
        return verified
    note = data.get('note')
    audio = request.FILES.get('audio')
    if note is None or note.strip() == '':
        return {
            'error':'note is required',
            'status':status.HTTP_400_BAD_REQUEST
        }
    notee = note.strip()
    new_assign = Assignment.objects.create(note=notee, session=session)
    
    if audio is not None:
        audi = audio_c.convert_audio(audio, new_assign)
        if audi.get('error') is not  None:
            return audi
    return {
        'id':new_assign.pk,
        'note':new_assign.note,
        'audio': get_image_url(new_assign),
        'status':status.HTTP_201_CREATED
    }