from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions,generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from .models import Comment, Animal, GalleryPhoto
from rest_framework import viewsets





from .models import Message
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    MessageSerializer,
    CommentSerializer,
    AnimalSerializer,
    GalleryPhotoSerializer
)

# Register View
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User registered successfully!",
                "username": user.username,
                "email": user.email,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login View
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(): 
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful!",
                "username": user.username,
                "email": user.email,
                "is_staff": user.is_staff,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all().order_by('timestamp')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_like(request, pk):
    try:
        message = Message.objects.get(pk=pk)
    except Message.DoesNotExist:
        return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if user in message.likes.all():
        message.likes.remove(user)
    else:
        message.likes.add(user)

    return Response({'likes': [u.id for u in message.likes.all()]})

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        message_id = self.kwargs['message_id']
        return Comment.objects.filter(message_id=message_id).order_by('-timestamp')

    def perform_create(self, serializer):
        message_id = self.kwargs['message_id']
        serializer.save(user=self.request.user, message_id=message_id)

class AnimalListCreateView(generics.ListCreateAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save()  


class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__iexact=category)
        return queryset

@api_view(['GET'])
def get_animals_by_category(request, category):
    animals = Animal.objects.filter(category__iexact=category)
    if animals.exists():
        serializer = AnimalSerializer(animals, many=True)
        return Response({
            "category": category,
            "animals": serializer.data
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "message": f"No animals found in category '{category}'"
        }, status=status.HTTP_404_NOT_FOUND)
   
class GalleryPhotoUploadView(generics.ListCreateAPIView):
    queryset = GalleryPhoto.objects.all().order_by("-uploaded_at")
    serializer_class = GalleryPhotoSerializer

# views.py
@api_view(['DELETE'])
@permission_classes([IsAdminUser])  # Only admins can delete
def delete_message(request, pk):
    try:
        message = Message.objects.get(pk=pk)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
