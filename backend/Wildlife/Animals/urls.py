from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    MessageListCreateView,
    toggle_like,
    CommentListCreateView,
    AnimalListCreateView,
    get_animals_by_category,
    GalleryPhotoUploadView,
    delete_message
    
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/like/', toggle_like, name='toggle_like'),
    path('messages/<int:message_id>/comments/', CommentListCreateView.as_view(), name='message-comments'),
    path('animals/', AnimalListCreateView.as_view(), name='animal-list-create'),
    path('animals/category/<str:category>/', get_animals_by_category, name='animals-by-category'),
    path("gallery/", GalleryPhotoUploadView.as_view(), name="gallery-upload"),
    path('messages/<int:pk>/delete/', delete_message, name='delete-message'),

]
