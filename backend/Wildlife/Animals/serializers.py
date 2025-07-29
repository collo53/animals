from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import Message,Comment, Animal,GalleryPhoto
import json


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        validate_password(data['password'])
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")
        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        data['user'] = user
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','is_staff']

class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'user', 'content', 'image', 'timestamp', 'likes']

    def get_likes(self, obj):
        return [user.id for user in obj.likes.all()]
   
class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_name', 'text', 'timestamp']
        extra_kwargs = {
            'user': {'read_only': True},
            'text': {'required': True},
            'message': {'required': False},  
        }

class FactsField(serializers.Field):
    def to_internal_value(self, data):
        # Accept a JSON string or a list
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                raise serializers.ValidationError("Facts must be a valid JSON string.")
        
        if not isinstance(data, list):
            raise serializers.ValidationError("Facts must be a list.")
        
        if not all(isinstance(item, str) for item in data):
            raise serializers.ValidationError("Each fact must be a string.")

        return data

    def to_representation(self, value):
        return value  # stored as list; return as-is

class AnimalSerializer(serializers.ModelSerializer):
    facts = FactsField(required=False)  # 🔄 Use the custom field here

    class Meta:
        model = Animal
        fields = '__all__'

class GalleryPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryPhoto
        fields = '__all__'

   
