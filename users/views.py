from django.contrib.auth import authenticate, login ,logout
from users.models import CustomUser
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to register

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({'msg':'User registered successfully','refresh': str(refresh),'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role')

        user = authenticate(username=email,email=email, password=password ,role=role)
        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({'msg':'Login successfully','refresh': str(refresh),'access': str(refresh.access_token),}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()  # This is the correct way to invalidate the token

            return Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            print("Error:", e)
            return Response({"detail": "Error logging out"}, status=status.HTTP_400_BAD_REQUEST)






