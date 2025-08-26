from class_session.models import ClassSession
from rest_framework import status
from class_session.utils import verify_admin, audio_c, valid_type
from assignment.models import Assignment
from django.conf import settings
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from datetime import datetime
from django.core.exceptions import ValidationError

def showError(e):
    if hasattr(e, 'message'):
        return e.message
    if hasattr(e, 'messages'):
        return '; '.join(e.messages)
    return 'server error'

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
        assignment = Assignment.objects.get(pk=pk)
    except Assignment.DoesNotExist:
        return {
            'error':'Assignment is not available',
            'status':status.HTTP_404_NOT_FOUND
        }
    verified = verify_admin.verify(user, assignment.session.classroom)
    if verified.get('error') is not None:
        return verified
    note = data.get('note')
    audio = request.FILES.get('audio')
    if note:
        val = valid_type.validate(note, str, "note")
        if val.get('error'):
            return val
        if note.strip():
            notee = note.strip()
            assignment.note =notee
    if data.get('publish'):
        deadline = data.get('deadline')
        if not deadline:
            return {
                'error':'no deadline provided',
                'status':status.HTTP_400_BAD_REQUEST
            }
        val = parse_datetime(deadline)
        if val is None:
            return {
                'error':'invalid datetime format',
                'status':status.HTTP_400_BAD_REQUEST
            }
        print(f'{deadline}-{val}')
        val = make_aware(val)
        
        assignment.deadline = val
        assignment.is_published = True
    
    if audio is not None:
        audi = audio_c.convert_audio(audio, assignment)
        if audi.get('error') is not  None:
            return audi
    try:    
        assignment.save()
    except ValidationError as e:
        return {
            'error': showError(e),
            'status': status.HTTP_400_BAD_REQUEST
        }
    return {
        'id':assignment.pk,
        'note':assignment.note,
        'audio': get_image_url(assignment),
        'status':status.HTTP_200_OK
    }