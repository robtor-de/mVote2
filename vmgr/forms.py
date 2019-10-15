from vmgr.models import SongRequest
from django.forms import ModelForm
from django import forms

class PublishForm(ModelForm):
    class Meta:
        model = SongRequest
        fields = ['song_title', 'song_artist']
