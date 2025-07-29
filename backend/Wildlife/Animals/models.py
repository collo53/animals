from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='chat_images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_messages', blank=True)

    def __str__(self):
        return f'{self.user.username} at {self.timestamp}'
class Comment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.message.id}"


class Animal(models.Model):
    name = models.CharField(max_length=100)
    habitat = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    size = models.CharField(max_length=50, blank=True)
    diet = models.CharField(max_length=100, blank=True)
    lifespan = models.CharField(max_length=50, blank=True)
    facts = models.JSONField(default=list)
    conservation_status = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to='animal_images/', null=True, blank=True)  # ✅ New

class GalleryPhoto(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="gallery_photos/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
