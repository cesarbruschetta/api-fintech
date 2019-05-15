
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import transaction

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


def get_token():
    """Create user on database and provide token for him.

    Returns:
        string: The token value.
     """
    user = User.objects.create_user('unittest', 'unittest@test.com', '!AT158r4yt9')            
    payload = JWT_PAYLOAD_HANDLER(user)
    token = JWT_ENCODE_HANDLER(payload)
    return "JWT " + token
