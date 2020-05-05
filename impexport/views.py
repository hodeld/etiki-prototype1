from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from django.urls import reverse
from django.utils import timezone

from impexport.Logic.ViewExport import exp_csv_nlp, exp_csv_basedata, extract_err_file
from impexport.Logic.ViewImportDB import parse_xcl
from impexport.Logic.ViewUpdateDB import update_internal


def export_csv_nlp(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    now = timezone.localtime()
    date_str = now.strftime('%Y%m%d')
    filename = 'impevs_nlp_' + date_str
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % filename
    response = exp_csv_nlp(response)

    return response


def export_csv_base(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    now = timezone.localtime()
    date_str = now.strftime('%Y%m%d')
    filename = 'base_nlp_' + date_str
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % filename
    response = exp_csv_basedata(response)

    return response


def export_csv_extr(request):
    response = HttpResponse(content_type='text/csv')
    now = timezone.localtime()
    date_str = now.strftime('%Y%m%d')
    filename = 'extracterr_' + date_str
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % filename
    response = extract_err_file(response)
    return response


@permission_required('etilog.impactevent')
def import_dbdata(request):  #
    parse_xcl()
    return HttpResponseRedirect(reverse('etilog:home'))


def update_db_internal(request):
    update_internal()
    return HttpResponseRedirect(reverse('etilog:home'))