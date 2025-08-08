from class_session.models import ClassSession, Lecture
from classroom.models import ClassMember, ClassRoom
from rest_framework import status
from django.conf import settings
import os
import uuid
from django.core.exceptions import ValidationError
from django.db import transaction
from .audio_c import convert_audio

def show_error(e):
    if hasattr(e,"message"):
        return e.message
    elif hasattr(e, "messages"):
        return "; ".join(e.messages)
    elif hasattr(e, "message_dict"):
        return e.message_dict
    else:
        return "unexpected error"

def post(request, class_r):
    user = request.user
    if not user.is_authenticated:
        return {
            'error': 'you are not logged in',
            'status':status.HTTP_401_UNAUTHORIZED
        }
    try:
        classroom = ClassRoom.objects.get(room_id=class_r)
    except ClassRoom.DoesNotExist:
        return {
            'error': 'classroom id is invalid',
            'status':status.HTTP_404_NOT_FOUND
        }
    try:
        member = ClassMember.objects.get(user=user, classroom=classroom, is_approved=True)
    except ClassMember.DoesNotExist:
        return {
            'error': 'You Are Not A Member',
            'status':status.HTTP_401_UNAUTHORIZED
        }
    if not member.role == 'admin' and not classroom.creator == user:
        print(member.role)
        print(classroom.creator.username)
        print(user.username)
        return {
            'error': 'only thw admin and class creator can create a session',
            'status':status.HTTP_401_UNAUTHORIZED
        }
    data = request.data
    topic = data.get("topic")
    note = data.get('note')
    audio = request.FILES.get("audio")
    
    if (not topic or topic.strip() == "") or (not note or note.strip() == ""):
        return {
            'error': 'topic and note are required',
            'status':status.HTTP_400_BAD_REQUEST
        }
        
    try:
        with transaction.atomic():
            session = ClassSession.objects.create(classroom=classroom)
            is_done = False
            lec = Lecture.objects.create(session=session, topic=topic, note=note)
            is_done = True
            if not is_done:
                raise ValidationError("Could not create the session, try again")
    except ValidationError as e:
        return {
            "errror": show_error(e)
        }
    if audio:
        audi = convert_audio(audio, lec)
        if audi.get('error'):
            return audi
    return {
        "session_id":session.pk,
        "lecture_id":lec.pk,
        "status":status.HTTP_201_CREATED
    }

    