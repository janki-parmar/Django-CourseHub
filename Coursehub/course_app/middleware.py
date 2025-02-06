import jwt
import datetime
from .models import *
import logging
logger = logging.getLogger(__name__)

def encode_jwt(user):

    expiry_time = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    
    # Convert the datetime object to a Unix timestamp (seconds since epoch)
    expiry_timestamp = int(expiry_time.timestamp())

    payload = {
            'id':user.id,
            'role': user.role,
            'exp': expiry_timestamp}

    encoded_token= jwt.encode(payload, 'secret_key', algorithm='HS256')
    print ("token=---------------", encoded_token)
    return encoded_token


def decode_jwt(token):

    payload = token

    try:
        decoded_token = jwt.decode(payload, 'secret_key', algorithm='HS256')
        print ("token=---------------", decoded_token)
        return decoded_token
    
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")


# class RoleBasedAccessMiddleware:

#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         token = request.headers.get('Authorization', None)

#         if token:
#             token = token.replace("Bearer ", "")
#             try:
#                 payload = decode_jwt(token)
#                 request.user_id = payload['id']
#                 request.user_role = payload['role']
#             except Exception as e:
#                 logger.error(f"Error during JWT decoding: {str(e)}")
#         else:
#             logger.error("Authorization token is required")

#         response = self.get_response(request)
#         return response

def role_based_access(view_func):
    from functools import wraps
    from django.http import JsonResponse

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.headers.get('Authorization', None)

        # Print token for debugging
        print(f"Token from headers: {token}")

        if not token:
            token = request.POST.get('auth_token', None)

        # Print token from POST for debugging
        print(f"Token from POST: {token}")

        if token:
            token = token.replace("Bearer ", "")  # Clean the token if 'Bearer' is included
            try:
                payload = decode_jwt(token)
                request.user_id = payload['id']
                request.user_role = payload['role']
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=401)
        else:
            return JsonResponse({'error': 'Authorization token is required'}, status=401)

        return view_func(request, *args, **kwargs)

    return _wrapped_view

