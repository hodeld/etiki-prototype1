from django.contrib.auth import logout
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import json

#forms
from django.urls import reverse

from etikihead.forms import ContactForm

# Create your views here.
from etilog.forms.forms_filter import NewSource
from etilog.models import FrequentAskedQuestions


def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name_visitor']
            new_subject = 'contactform – ' + form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            line_break = ' '.join(('\n', '\n', '–––– original message ––––', '\n', '\n'))
            full_message = ' '.join(('message from:', name, line_break,
                                     message)
                                    )
            try:
                send_mail(new_subject, full_message, from_email, ['info@etiki.org'])
                form.save()
                msg = ' '.join(('Thank you for your message,', name))
            except BadHeaderError:
                m = form.save(commit=False)
                m.sent_to_etiki = False
                m.save()
                msg = 'Invalid header found. Try again.'
        else:
            msg = 'There was an error, please try again. Sorry.'
        d_dict = {'msg': msg}
        jsondata = json.dumps(d_dict)
        return HttpResponse(jsondata, content_type='application/json')

    return render(request, 'etikihead/contact.html', {'form': form})


def entry_mask(request):
    return render(request, 'etikihead/entrymask/main.html', )


def legal(request):
    return render(request, 'etikihead/legal.html', )


def about(request):
    return render(request, 'etikihead/about.html', )


def faq(request):
    faqs = FrequentAskedQuestions.objects.all().order_by('question')
    return render(request, 'etikihead/faq.html', {'faqs': faqs})


def startinfo(request):
    if request.method == 'POST':
        form = NewSource(request.POST)
        if form.is_valid():
            form.save()
            print('valid', form.cleaned_data)
            message = 'you are helping creating a new platform, thank you!'
        else:
            message = 'oh, this did not work!'

    else:
        message = ''
    form = NewSource()
    return render(request, 'etikihead/comingsoon.html', {'form': form,
                                                      'message': message
                                                      })