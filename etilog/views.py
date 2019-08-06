from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

#from 3rd apps
from django_tables2 import RequestConfig

#models
from .models import ImpactEvent
#tables
from .tables import ImpEvTable
#forms
from .forms import NewImpactEvent, NewSource

#viewlogic
from etilog.ViewLogic.ViewImportDB import parse_xcl

# Create your views here.
def startinfo(request):
    
    if request.method == 'POST':
        form = NewSource(request.POST)
        if form.is_valid():
            form.save() 
            print('valid', form.cleaned_data)
            message = 'thank you!'
        else:
            message = 'oh, this did not work!'
    
    else:
        message = ''
    form = NewSource()
    return render(request, 'etilog/start.html', {'form': form,
                                                 'message': message
                                                             })

def overview_impevs(request):
    
    table = ImpEvTable(ImpactEvent.objects.all())
    #table.order_by = 'start'
    RequestConfig(request, paginate={'per_page': 20}).configure(table) 
    
    return render(request, 'etilog/impactevents_overview.html', {'table': table})

def import_dbdata(request):
    
    parse_xcl()
    return HttpResponseRedirect(reverse('etilog:home'))

def new_impact_event(request):
    if request.method == 'POST':
        pass
    
    else:
        pass
    form = NewImpactEvent()
    
    return render(request, 'etilog/newimpactevent.html', {'form': form,
                                                             })
        
    