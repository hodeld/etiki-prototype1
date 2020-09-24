import json
import os
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from prediki.predictText.main import analyze_text, sentiment_predict, multi_predict_text


def predict_text(request, text):
    def get_path(n):
        if settings.DEBUG:
            #base_dir = os.path.dirname(settings.BASE_DIR)
            #model_def = os.path.join(base_dir, 'prediki/static/prediki/model_data/')
            model_def = settings.MODEL_DEF
            p = os.path.join(model_def, n)
        else:
            p = staticfiles_storage.path('prediki/model_data/' + n)
        return p
    
    #text = request.POST.get('text')
    p_senti = get_path('sentiment')
    tend_id = sentiment_predict(text, p_senti)
    p_multi = get_path('multi')
    cat_id = multi_predict_text(text, p_multi)

    d_dict = {'cat_id': cat_id,
           'tend_id': tend_id}
    return HttpResponse(json.dumps(d_dict), content_type='application/json')
