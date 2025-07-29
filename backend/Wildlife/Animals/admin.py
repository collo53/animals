from django.contrib import admin
from .models import Message, Comment, Animal,GalleryPhoto

admin.site.register(Message)  
admin.site.register(Comment)
admin.site.register(Animal)  
admin.site.register(GalleryPhoto) 