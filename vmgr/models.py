from django.db import models

class SongRequest(models.Model):
    song_title = models.CharField(max_length=40)
    song_artist = models.CharField(max_length=40)
    votes = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
