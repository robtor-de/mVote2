from django.shortcuts import render
from vmgr.forms import PublishForm
from django.http import HttpResponse, HttpResponseRedirect
from vmgr.models import SongRequest

def publish_song(request):

    if request.method == 'POST':
        form = PublishForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse("ok")
    else:
        form = PublishForm()
        return render(request, "publish_song.htm", {'form' : form})


#Show complete list with votable Songs and already accepted enqued songs
def vote(request):
    #retrieve a list of votable songs
    votable = SongRequest.objects.filter(completed=False, accepted=False).order_by('votes')
    com_pks = request.session.keys()

    #retrieve a list of already accepted not removed Songs
    waiting = SongRequest.objects.filter(completed=False, accepted=True)

    #retrieve a list of removed Songs
    completed = SongRequest.objects.filter(completed=True)


    return render(request, "votelist.htm", {'votable': votable, 'waiting': waiting, 'completed': completed})

def countvote(request, pkey=0):
    if pkey != 0:
        vmodel = SongRequest.objects.get(pk=pkey)

        if(pkey not in request.session):
            request.session[pkey] = False

        if vmodel.completed == False and request.session[pkey] == False:
            vmodel.votes = vmodel.votes + 1
            vmodel.save()

            request.session[pkey] = True
            return HttpResponseRedirect("/vote")
        elif request.session[pkey] == True:
            return HttpResponse("Schon abgestimmt")
        else:
            return HttpResponse("Nicht mehr aktiv")
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
