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


def vote(request):

    active = SongRequest.objects.filter(completed=False)
    completed = SongRequest.objects.filter(accepted=True)

    return render(request, "votelist.htm", {'active': active})

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
