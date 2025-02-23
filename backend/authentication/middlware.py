
import base64, datetime
# from models import User

# class AuthMiddlware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#     def __call__(self, request):

#         if hasattr(request.COOKIE, 'access_token'):
#             token = request.COOKIE.get('access_token')
#             if not token:
#                 raise Exception('No token found')
#             payload = token.split('.')[1]
#             id = base64.urlsafe_B64decode(payload).decode('utf-8')['user_id']
#             exp = base64.urlsafe_B64decode(payload).decode('utf-8')['exp']
#             user = User.objects.get(id=id)
#             if not user:
#                 raise  Exception('User not found')
#             if datetime.datetime.utcnow() > exp:
#                 raise Exception('Token expired')
#             request.Cookie['access_token'] = token
#         # response = self.get_response()
#         return response