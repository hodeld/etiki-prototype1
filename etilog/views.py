from django.shortcuts import render

# Create your views here.
def overview_impevs(request):
    
    return render(request, 'etilog/start.html')