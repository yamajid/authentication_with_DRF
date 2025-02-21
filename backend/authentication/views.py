from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from dotenv import load_dotenv
import base64, json, datetime, jwt, os, hmac, hashlib

User = get_user_model()
load_dotenv()


class UserRegister(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'user logged successfully'}, status=201)


class UserLogin(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not password or not username:
            return Response({'username and password required'}, status=400)
        try: 
            user = get_object_or_404(User, username=username)
            user.check_password(password)
        except:
            return Response({'error': 'user not found'}, status=404)
        response = Response({
            'user': user.username,
        })
        secret_key = os.getenv('JWT_SECRET_KEY')
        access_token = generate_access_token(secret_key)
        refresh_token = generate_refresh_token(secret_key)
        access_token  = access_token.create_token(user)
        refresh_token = refresh_token.create_token(user)
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=False, path='/')
        response.set_cookie(key='access_token', value=access_token, httponly=False, path='/')
        return response
        
        
class generate_access_token:


    def __init__(self, secret):
        self.secret_key = secret
        
    def create_token(self, user):

        header = {
            'alg': 'HS256',
            'typ': 'access',
        }

        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp' : f'{datetime.datetime.utcnow() + datetime.timedelta(minutes=5)}'

        }
        header = base64.urlsafe_b64encode(json.dumps(header).encode('utf-8')).decode('utf-8').replace('=', '')
        payload = base64.urlsafe_b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8').replace('=', '')
        sign_input = f'{header}.{payload}'.encode('utf-8')
        hash_object = hmac.new(f'{self.secret_key}'.encode('utf-8'), sign_input, hashlib.sha256).digest()
        signature = base64.urlsafe_b64encode(hash_object).decode('utf-8').replace('=', '')
        token = f'{header}.{payload}.{signature}'
        return token

class generate_refresh_token:


    def __init__(self, secret):
        self.secret_key = secret
        
    def create_token(self, user):

        header = {
            'alg': 'HS256',
            'typ': 'refresh',
        }

        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp' : f'{datetime.datetime.utcnow() + datetime.timedelta(days=120)}'

        }
        header = base64.urlsafe_b64encode(json.dumps(header).encode('utf-8')).decode('utf-8').replace('=', '')
        payload = base64.urlsafe_b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8').replace('=', '')
        sign_input = f'{header}.{payload}'.encode('utf-8')
        hash_object = hmac.new(f'{self.secret_key}'.encode('utf-8'), sign_input, hashlib.sha256).digest()
        signature = base64.urlsafe_b64encode(hash_object).decode('utf-8').replace('=', '')
        token = f'{header}.{payload}.{signature}'
        return token
     

class UserLogout(APIView):
    def post(self, request):
        response = Response({
            'message': 'User logged out successfully'
        })
        response.cookie_blacklist(key='refresh_token')
        response.cookie_blacklist(key='access_token')
        return response
        
        

# Create your views here.
1