from django.conf.urls import url
from django.contrib import admin
from bot.views import ChatterBotAppView, ChatterBotApiView

app_name = 'bot'

urlpatterns = [
    url(r'^$', ChatterBotAppView.as_view(), name='main'),
    url(r'^api/chatterbot/', ChatterBotApiView.as_view(), name='chatterbot'),
]
