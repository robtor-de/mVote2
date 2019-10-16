from django.shortcuts import render
from vmgr.forms import PublishForm
from django.http import HttpResponse, HttpResponseRedirect
from vmgr.models import SongRequest, Voice
from django.db.models import Value
import math

def start(request):
    if request.session.get("intro", False):
        return HttpResponseRedirect("/vote/")
    else:
        request.session["intro"] = True
        return render(request, "start.htm")

def publish_song(request):

    if request.method == 'POST':
        form = PublishForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/vote/")
    else:
        form = PublishForm()
        form.fields['song_title'].widget.attrs.update({'class': 'form-control'})
        form.fields['song_artist'].widget.attrs.update({'class': 'form-control'})
        return render(request, "publish_song.htm", {'form' : form})


#Show complete list with votable Songs and already accepted enqued songs
def vote(request):
    if not request.session.session_key:
        request.session.save()

    #retrieve a list of votable songs
    votable = SongRequest.objects.filter(completed=False, accepted=False).order_by(Value('votes').desc())

    songs = []
    status = []
    percentage = []

    cvotes = 0
    for element in votable:
        cvotes += element.voice_set.all().count()

    for element in votable:
        try:
            percentage.append(math.floor((element.voice_set.all().count()/cvotes)*100))
        except:
            percentage.append(0)
        songs.append(element)
        if element.voice_set.filter(skey=request.session.session_key).exists():
            status.append(True)
        else:
            status.append(False)

    vlist = zip(songs, status, percentage)

    #retrieve a list of already accepted not removed Songs
    waiting = SongRequest.objects.filter(completed=False, accepted=True)

    #retrieve a list of removed Songs
    completed = SongRequest.objects.filter(completed=True)


    return render(request, "votelist.htm", {'vlist': vlist, 'waiting': waiting, 'completed': completed})

def countvote(request, pkey=0):
    if not request.session.session_key:
        request.session.save()


    if pkey != 0:

        try:
            vmodel = SongRequest.objects.get(pk=pkey)

            if(vmodel.voice_set.filter(skey=request.session.session_key).exists()):
                return HttpResponse("Schon abgestimmt")
            else:
                try:
                    voice = Voice(songrequest=vmodel, skey=request.session.session_key)
                    voice.save()
                except:
                    return HttpResponse("Fehler beim Speichern der Stimme")
                vmodel.votes = vmodel.votes + 1
                vmodel.save()
                return HttpResponseRedirect("/vote/")
        except:
            return HttpResponse("Fehler, angefragter SongRequest existiert nicht")

    else:
        return HttpResponse("Fehler")

def results(request):
    songstoplay = SongRequest.objects.filter(completed=False, accepted=True).order_by('votes')
    songstomanage = SongRequest.objects.filter(completed=False, accepted=False).order_by('votes')

    return render(request, "resultlist.htm", {'songstoplay': songstoplay, 'songstomanage': songstomanage})

def completevote(request, pkey):
    r = SongRequest.objects.get(pk=pkey)
    r.completed = True
    r.save()
    return HttpResponseRedirect("/voteresults/")

def acceptvote(request, pkey):
    r = SongRequest.objects.get(pk=pkey)
    r.accepted = True
    r.save()
    return HttpResponseRedirect("/voteresults/")
