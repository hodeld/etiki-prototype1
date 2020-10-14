import json

from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from etikicapture.views import error_handling
from usermgmt.forms import UserForm, UserCreateForm


@login_required
def profile(request, user_name=None):
    user = request.user
    if request.user.is_authenticated:
        user = request.user
        userform = UserForm(instance=user)
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


def change_password(request):
    if request.method == 'POST':
        d_dict = {}
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            d_dict['message'] = 'Your password was successfully updated!'
            return redirect('change_password')
        else:
            d_dict['message'] = 'Please correct the error below.'
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('usermgmt:login'))
    # Redirect to a success page.


def create_user(request):
    form = UserCreateForm()
    return render(request, 'usermgmt/profile.html',
                  {'form': form,  # for form.media
                   'user': None
                   })


def create_user_save(request):

    form = UserCreateForm(request.POST)
    d_dict = {}
    if form.is_valid():
        user = form.save()
        #update_session_auth_hash(request, user)
        login(request, user)
        d_dict['message'] = 'success'
        status_code = None  # 200
        d_dict['redirect'] = reverse('usermgmt:profile', kwargs={'user_name': user.username})
    else:
        d_dict['message'] = 'error'
        status_code = 406  # not acceptable
        error_handling(form, d_dict)
    return HttpResponse(json.dumps(d_dict), content_type='application/json', status=status_code)

