from class_session.models import ClassSession, Lecture, Image
import os
import uuid
from pydub import AudioSegment
from django.contrib.contenttypes.models import ContentType
from classroom.models import ClassMember
from rest_framework import status
from django.conf import settings
from django.core.files import File
from PIL import Image as PILImage
from io import BytesIO
from django.core.files.base import ContentFile

def convert_to_webp(uploaded_file, quality=80):
    img = PILImage.open(uploaded_file)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    buffer = BytesIO()
    img.save(buffer, format="WEBP", quality=quality)
    return ContentFile(buffer.getvalue(), name=os.path.splitext(uploaded_file.name)[0] + ".webp")


def get_image_url(img):
    if settings.DEBUG:
        return f"{settings.HOST_URL}{img.file.url}"
    else:
        return img.file.url

def post(request, pk):
    user = request.user
    payload = request.data
    
    if not user.is_authenticated:
        return {
            'error': 'you are not logged in',
            'status':status.HTTP_401_UNAUTHORIZED
        }
    try:
       session = ClassSession.objects.select_related("lecture").get(pk=pk)
    except ClassSession.DoesNotExist:
        return {
            'error': 'class session does not exist',
            'status':status.HTTP_404_NOT_FOUND
        }
    try:
        member = ClassMember.objects.get(user=user, classroom=session.classroom, is_approved=True)
    except ClassMember.DoesNotExist:
        return {
            'error': 'You Are Not A Member',
            'status':status.HTTP_401_UNAUTHORIZED
        }
        
    if session.is_published:
        return {
            'error': 'Public session cannot be edited',
            'status':status.HTTP_401_UNAUTHORIZED
        }
        
    lecture = session.lecture
    topic = payload.get("topic")
    note = payload.get("note")
    audio = request.FILES.get("audio")
    images = request.FILES.get('image')
    _file = request.FILES.get('file')
    content_t = ContentType.objects.get_for_model(lecture)
    
    if topic and topic.strip() != "":
        top = topic.strip()
        lecture.topic = top
        
    if note and note.strip() != "":
        nott = note.strip()
        lecture.note = nott
        
    if audio:
        try:
            #save the file on temp path
            temp_path = os.path.join(settings.MEDIA_ROOT, 'temp/audio/raw', f'{uuid.uuid4()}_{audio.name}')
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            with open(temp_path, 'wb+') as file:
                for chunk in audio.chunks():
                    file.write(chunk)
            #get file extension and convert
            ext = os.path.splitext(temp_path)[1].lower().replace('.', '')
            input_format = 'wav' if ext == 'wav' else ext or 'webm'
            sound = AudioSegment.from_file(temp_path, format=input_format)
            # convert and save
            output_filename = f"{uuid.uuid4()}.wav"
            output_path = os.path.join(settings.MEDIA_ROOT, 'temp/audio/converted', output_filename )
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            sound.export(output_path, format='wav')
            with open(output_path, "rb") as output:
                lecture.audio.save(output_filename, File(output))
            os.remove(temp_path)
            os.remove(output_path)
        except Exception as e:
            print(str(e))
            return {
                'error': 'Something went wrong during audio handling, please try again',
                'status':status.HTTP_400_BAD_REQUEST
            }
    
    if images:
       
        try:
            tag = payload.get("img_tag", "")
            image = Image.objects.create(
                session=session,
                tag=tag,
                file=convert_to_webp(images),
                content_type=content_t,
                object_id=lecture.pk, 
            )
        except Exception as e:
            print(str(e))
            return {
                'error': 'Something went wrong while process the image, try again',
                'status':status.HTTP_400_BAD_REQUEST
            }
    
    if _file:
       
        try:
            tag = payload.get("file_tag", "")
            fil = File.objects.create(
                session=session,
                tag=tag,
                file=_file,
                content_type=content_t,
                object_id=lecture.pk, 
            )
        except Exception as e:
            print(str(e))
            return {
                'error': 'Something went wrong while process the file, try again',
                'status':status.HTTP_400_BAD_REQUEST
            }
    
    lecture.save()
    return {
        "message":"created",
        "id":session.pk,
        "status":status.HTTP_200_OK
    }
       