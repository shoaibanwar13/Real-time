from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard_view/', dashboard_view, name='import_excel'),
    path('', home,name="home"),
    path("send_chat_message",send_chat_message,name="send_chat_message")
]

