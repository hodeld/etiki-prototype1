import json

from django.contrib.auth import logout
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from etikicapture.views import error_handling
from usermgmt.forms import UserForm


@permission_required('etilog.impactevent')
def profile(request, user_name=None):
    user = request.user
    if request.user.is_authenticated:
        user = request.user
        userform = UserForm(instance=user)
    else:
        userform = UserForm()
    return render(request, 'usermgmt/profile.html',
                  {'form': userform,  # for form.media
                   'user': user
                   })

def profile_update(request):
    user = request.user
    d_dict = {}
    form = UserForm(data=request.POST, instance=user)
    if form.is_valid():
        form.save()
        d_dict['is_valid'] = 'true'
        d_dict['message'] = 'User %s updated' % user.username

    else:
        d_dict['message'] = 'error'
        error_handling(form, d_dict)
    return HttpResponse(json.dumps(d_dict), content_type='application/json')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('usermgmt:login'))
    # Redirect to a success page.