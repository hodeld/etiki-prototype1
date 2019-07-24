from django.shortcuts import render
#models
from .models import ImpactEvent
#tables
from .tables import ImpEvTable

# Create your views here.
def startinfo(request):
    
    return render(request, 'etilog/start.html')

def overview_impevs(request):
    
    table = ImpEvTable(ImpactEvent.objects.all())
    
    return render(request, 'etilog/impactevents_overview.html', {'table': table})