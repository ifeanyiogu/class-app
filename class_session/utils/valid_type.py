from rest_framework import status

def validate(obj, opt, mes):
    if not isinstance(obj,opt):
        return {
            'error':f'{mes} is invalid',
            'status':status.HTTP_400_BAD_REQUEST
        }
    return {}