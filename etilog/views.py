from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
#models
from .models import ImpactEvent
#tables
from .tables import ImpEvTable

#viewlogic
from etilog.ViewLogic.ViewImportDB import parse_xcl

# Create your views here.
def startinfo(request):
    
    return render(request, 'etilog/start.html')

def overview_impevs(request):
    
    table = ImpEvTable(ImpactEvent.objects.all())
    
    return render(request, 'etilog/impactevents_overview.html', {'table': table})

def import_dbdata(request):
    
    parse_xcl()
    return HttpResponseRedirect(reverse('etilog:home'))
    