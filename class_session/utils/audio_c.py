import os
import uuid
from pydub import AudioSegment
from django.core.files import File
from rest_framework import status

def convert_audio(audio, lecture):
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
    return {'message':True}