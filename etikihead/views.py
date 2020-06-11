from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
import json

#forms
from etikihead.forms import ContactForm

# Create your views here.


def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name_visitor']
            new_subject = 'contactform –' + form.cleaned_data['subject']
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