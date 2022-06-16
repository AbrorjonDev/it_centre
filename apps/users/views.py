from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth.mixins import UserPassesTestMixin

from django.contrib.auth import get_user_model
User = get_user_model()
#local imports
from .serializers import (
    UserSerializer,
    PasswordChangeSerializer,

)

class LoginAPIView(APIView):
    """
    Get token in here.
    In POST:
        username: str
        password: BaseModelstr
    """
    queryset = None
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"detail":"Not Authenticated"}, status=401)            
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user":self.serializer_class(user, many=False).data
        }, status=200)


class PasswordChangeView(APIView):
    """
    Users can change their passwords with new one.
    User token is required.

    In POST:
        old_password: str,
        new_password1: str,
        new_password2: str
    """
    serializer_class = PasswordChangeSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request":request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"detail":"password changed succesfully."}, status=200)
        return Response({"detail":"error occured."}, status=400)

        


class UserAPIView(APIView, UserPassesTestMixin):
    """
    All user objects in here.
    If you are a director, you can see and add only your admins.
    If you are a developer, you can see and add all users.

    In POST:
        username: str,
        password: str,

    If you are a developer, then add one of these params:
        is_admin: str,
        is_director: str 
    """

    def get_queryset(self, user=None):
        if user and user.is_superuser:
            return User.objects.all()
        elif user and user.is_director:
            return User.objects.filter(created_by=user)
        elif user and user.is_admin:
            return User.objects.filter(created_by=user.created_by)

    serializer_class = UserSerializer

    def get(self, request):
        serializer = self.serializer_class(self.get_queryset(user=request.user), many=True) 
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request":request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_director

class UserDetailAPIView(APIView, UserPassesTestMixin):
    """
    Directors and superusers can only edit admins.
    If you are a superuser, you can update also directors.
    
    In POST:
        username: str,
        password: str,
        is_director: str,
        is_admin: str
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = self.serializer_class(user, many=False)
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = self.serializer_class(user, data=request.data, partial=True, context={"request":request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user:
            user.delete()
            return Response({"detail":"deleted succesfully."}, status=200)
        return Response({"detail":"Not found"}, status=400)

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_director