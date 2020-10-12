import json

from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.shortcuts import render

from usermgmt.forms import UserForm


@permission_required('etilog.impactevent')
def profile(request, user_id=None):
    user = request.user

    userform = UserForm(instance=user)
    return render(request, 'usermgmt/profile.html',
                  {'form': userform,  # for form.media
                   'user': user
                   })

def profile_update(request):
    user = request.user
    d_dict = {}
    form = UserForm(instance=user)
    if form.is_valid():
        newie = form.save()
        newie_id = newie.pk
        d_dict['is_valid'] = 'true'
        d_dict['message'] = 'User %s updated' % user.username

    else:
        d_dict['message'] = 'error'
        #error_handling(form, d_dict)
    return HttpResponse(json.dumps(d_dict), content_type='application/json')

