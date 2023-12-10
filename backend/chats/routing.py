from django.urls import re_path, path

from chats import consumers

websocket_urlpatterns = [
    path("contracts/<int:contract_id>/<int:user_id>/<str:token>/", consumers.ChatConsumer.as_asgi()),
]
