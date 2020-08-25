import json

from crispy_forms.utils import render_crispy_form
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.context_processors import csrf
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy

from etikicapture.ViewLogic.ViewAccessURL import parse_url, parse_url_all, extract_text_rpy
from etikicapture.forms import ImpactEventForm, CompanyForm, ReferenceForm, TopicTagsForm
#models
from etilog.models import ImpactEvent, Company, Reference, SustainabilityTag


@permission_required('etilog.impactevent')
def extract_text(request, ie_id=None):
    try:
        ie = ImpactEvent.objects.get(id=ie_id)
    except ImpactEvent.DoesNotExist:
        return HttpResponseRedirect(reverse('etilog:home'))
    parse_url(ie)

    return HttpResponseRedirect(reverse('etilog:home'))


@permission_required('etilog.impactevent')
def extract_text_all(request):
    parse_url_all()
    return HttpResponseRedirect(reverse('etilog:home'))


def extract_text_from_url(request):
    url = request.GET.get('sourceurl')
    d_dict = {}
    parse_res = 0
    if url is not '':
        save_article, parse_res, article = extract_text_rpy(url)
    else:
        save_article = False
    if save_article == True:
        msg = 'extracted'
        text_str, stitle, sdate, html_simple = article
        impev_d = {'pk':0,
                   'source_url': url,
                   'article_title': stitle,
                   'article_html': html_simple
                   }
        html_article = render_to_string('etilog/impev_details/impev_show_article.html', {'rec': impev_d,
                                                                                         })

        d_dict['is_valid'] = 'true'
        d_dict['stext'] = text_str
        d_dict['stitle'] = stitle
        d_dict['sdate'] = sdate
        d_dict['shtml'] = html_simple

        #for preview
        d_dict['html_article'] = html_article

    else:
        msg = 'not extracted'
    d_dict['parse_res'] = parse_res
    d_dict['message'] = msg
    return HttpResponse(json.dumps(d_dict), content_type='application/json')


# at permission_required('etilog.impactevent')
def impact_event_create(request, ie_id=None):
    if ie_id:
        ietype = 'copy'
    else:
        ietype = 'new'
    response = impact_event_change(request, ietype=ietype, ie_id=ie_id)
    return response


@permission_required('etilog.impactevent')
def impact_event_update(request, ietype='new', ie_id=None):
    ietype = 'update'
    response = impact_event_change(request, ietype=ietype, ie_id=ie_id)
    return response


def impact_event_change(request, ietype='new', ie_id=None):
    shtml = ''
    data_dict = get_ie_form_data(request)
    if request.method == 'POST':
        #data_dict = get_ie_form_data(request)
        if ietype == 'update':
            message = 'Impact Event updated'
            ie = ImpactEvent.objects.get(id=ie_id)
            form = ImpactEventForm(data_dict, instance=ie, request=request)  # if ie = None
        else:  # new / new from copy
            message = 'Impact Event saved'
            form = ImpactEventForm(data_dict, request=request)

        to_json = {}
        if form.is_valid():
            newie = form.save()
            newie_id = newie.pk
            to_json['is_valid'] = 'true'
            to_json['message'] = message
            update_url = reverse('etikicapture:impactevent_update', kwargs={'ie_id': newie_id})
            to_json['upd_url'] = update_url


        else:
            error_handling(form, to_json)
        return HttpResponse(json.dumps(to_json), content_type='application/json')

    else:
        message = ''
        init_data = {}
        if ietype == 'update':
            init_data = get_ie_init_data(ie_id, update=True)
            next_id = ImpactEvent.objects.filter(id__gt=ie_id).order_by('id').values_list('id', flat=True).first()
            next_id_url = reverse_lazy('etikicapture:impactevent_update', kwargs={'ie_id': next_id})
        else:
            if ietype == 'copy':
                init_data = get_ie_init_data(ie_id, update=False)

            first_id = ImpactEvent.objects.order_by('id').values_list('id', flat=True).first()
            next_id_url = reverse_lazy('etikicapture:impactevent_update', kwargs={'ie_id': first_id})
        form = ImpactEventForm(initial=init_data, request=request)
        shtml = init_data.get('article_html', '')
    return render(request, 'etikicapture/impev_upd_base.html', {'form': form,  # for form.media
                                                          'message': message,
                                                          'next_id_url': next_id_url,
                                                          'shtml': shtml })


def get_ie_form_data(request):
    data_dict = request.POST.dict()

    upd_datadict_many(['sust_tags',], data_dict, request)
    if request.user:
        user_id = request.user.id
    else:
        user_id = None
    data_dict['user'] = user_id
    return data_dict


def get_ie_init_data(ie_id, update=False):
    init_data = {}
    impev = ImpactEvent.objects.get(id=ie_id)
    init_data['company'] = impev.company.name
    init_data['sust_domain'] = impev.sust_domain.id
    init_data['sust_tendency'] = impev.sust_tendency.id
    init_data['sust_tags'] = list(impev.sust_tags.all())
    init_data['summary'] = impev.summary
    if update:
        init_data['article_text'] = impev.article_text
        init_data['article_title'] = impev.article_title
        init_data['article_html'] = impev.article_html
        init_data['result_parse_html'] = impev.result_parse_html
        init_data['source_url'] = impev.source_url
        init_data['date_published'] = impev.date_published
        init_data['date_impact'] = impev.date_impact
        init_data['date_text'] = impev.date_text
        init_data['comment'] = impev.comment
        init_data['reference'] = impev.reference.name

    # form = ImpactEventForm(initial = init_data)
    return init_data


@permission_required('etilog.impactevent')
def add_foreignmodel(request, main_model, foreign_model):
    if request.POST:
        data_dict = request.POST.dict()
        if foreign_model == 'reference':
            form = ReferenceForm(data_dict)
        elif foreign_model == 'company':
            fieldlist = ['owner', 'subsidiary', 'supplier', 'recipient']
            upd_datadict_company(fieldlist, data_dict, request)
            form = CompanyForm(data_dict)
        else:  #tags
            upd_datadict_many(['sust_domains', ], data_dict, request)
            form = TopicTagsForm(data_dict)

        if form.is_valid():
            instance = form.save()  # (commit false) only needed if changes are done afterwards

            # handles the result of the foreign model in the original one
            d_dict = {
                'tag': {'id': instance.pk,
                        'name': str(instance),
                        'category': foreign_model},
                'is_valid': 'true',

            }
            jsondata = json.dumps(d_dict)
            return HttpResponse(jsondata, content_type='application/json')

        else:
            d_dict = {
            }
            error_handling(form, d_dict)
            jsondata = json.dumps(d_dict)
            return HttpResponse(jsondata, content_type='application/json')

    else:
        if foreign_model == 'reference':
            form = ReferenceForm()
        elif foreign_model == 'company':
            form = CompanyForm()
        else:
            form = TopicTagsForm()

    ctx = {}
    ctx.update(csrf(request))

    form_html = render_crispy_form(form, context=ctx)

    d_dict = form_html
    jsondata = json.dumps(d_dict)
    return HttpResponse(jsondata, content_type='application/json')


def upd_datadict_company(fieldlist, data_dict, request):
    """tagsinput to list"""
    for nam in fieldlist:
        if request.POST.get(nam):
            id_str_li = request.POST.get(nam)
            id_li = id_str_li.split(',')
            #id_li = request.POST.getlist(nam)
            data_dict[nam] = id_li


def upd_datadict_many(fieldlist, data_dict, request):
    for nam in fieldlist:
        if request.POST.get(nam):
            id_list = json.loads(request.POST.get(nam))
            data_dict[nam] = id_list



# used in New IE Form
def load_sust_tags(request):  # ,
    tendency_id_str = request.GET.get('categoryId')
    lookup_dict = {}

    def lookup_many(name_s, val):
        id_list = [int(val)]  # list
        lookup = '__'.join([name_s, 'in'])
        lookup_dict[lookup] = id_list

    def lookup_one(name_s, val):
        f_id = int(val)
        lookup_dict[name_s] = f_id

    if len(tendency_id_str) > 0:
        lookup_one('sust_tendency', tendency_id_str)
    domain_id_str = request.GET.get('domainId')
    if len(domain_id_str) > 0:
        lookup_many('sust_domains', domain_id_str)

    sust_tags = SustainabilityTag.objects.filter(**lookup_dict).order_by('name').values('id', 'name')


    data = json.dumps(list(sust_tags))
    return HttpResponse(data, content_type='application/json')


def error_handling(form, d_dict):
    message = form.errors.__html__()  # html
    err_items = dict(form.errors.items())
    d_dict['is_valid'] = 'false'
    d_dict['err_items'] = err_items
    d_dict['error_msg'] = message