from rest_framework import views
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import authentication
from users.models import User
from app.models import Task
from django.contrib.auth import logout as log_out
from django.contrib.auth.hashers import make_password, check_password
import logging

from .serializers import UserSerializer, TaskSerializer

logging.basicConfig(level=logging.DEBUG)

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    @action(detail=False, methods=['GET'])
    def profile(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class AuthViewset(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    
    @action(detail=False, methods=['POST'])
    def signup(self, request):
        serializer = UserSerializer(data=request.data)
        
        raw_password = request.data.get('password')
        hashed_password = make_password(raw_password)
        request.data['password'] = hashed_password

        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return Response({'detail': 'An account with that email already exists'}, status=status.HTTP_400_BAD_REQUEST)


        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    @action(detail=False, methods=['POST'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not User.objects.filter(email=email).exists():
            return Response({'detail': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = User.objects.get(email=email)

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({'access_token': access_token}, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

    @action(detail=False, methods=['GET'])
    def logout(self, request):        
        log_out(request)
        return Response({'detail': 'Logged Out'}, status=status.HTTP_200_OK)   


class AuthStatusView(views.APIView):
    permission_classes = [AllowAny]
    authentication_classes = [authentication.SessionAuthentication]

    def get(self, request, *args, **kwargs):
        return Response(True)

              
class TaskViewset(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(assigned_user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=False, methods=['POST'])
    def mark_competed(self, request):
        task = self.get_object()
        task.completed = True
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data)