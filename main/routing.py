from django.urls import re_path

from main import consumers

websocket_urlpatterns = [
    re_path(r"ws/upload/$", consumers.UploadConsumer.as_asgi())
]