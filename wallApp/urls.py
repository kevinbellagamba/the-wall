from django.urls import path, include
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path('', views.wallIndex),
    path('post', views.createPost),
    path('comment', views.createComment),
    path('<int:message_id>/delete', views.deleteMessage),
]
