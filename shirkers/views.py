from datetime import date
import json

from django.conf import settings
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView, TemplateView

from .models import Company, MissedMonths
from .helpers import calc_table_data


if hasattr(settings, 'STATIC_BASE_URL'):
    BASEURL = settings.STATIC_BASE_URL
else:
    BASEURL = ''


class Home(TemplateView):
    template_name = 'shirkers/index.html'
    num_hits = 10

    def find_companies(self, query):
        try:
            int(query)  # Checks if query is a number
            filtered = Company.objects.filter(
                vat_id__contains=query).distinct()[:self.num_hits]
        except:
            filtered = Company.objects.filter(
                name__icontains=query).distinct()[:self.num_hits]
        return filtered

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        companies = []
        if request.GET.get('term', None):
            question = request.GET.get('term', '')
            ctx['question'] = question
            companies = self.find_companies(question)

        if request.GET.get('format') == 'json':
            matches = json.dumps([
                {'id': x.vat_id, 'value': x.name} for x in companies
            ])
            return HttpResponse(matches, content_type='application/json')
        else:
            if len(companies) > 1:
                ctx['companies'] = companies
            elif len(companies) == 1:
                return HttpResponseRedirect(companies[0].get_absolute_url())
        return self.render_to_response(ctx)


class Embed(TemplateView):
    template_name = 'shirkers/embed.html'

    def get_context_data(self, **kwargs):
        ctx = {
            'BASEURL': BASEURL
        }
        return ctx


class IFrameEmbed(TemplateView):
    template_name = 'shirkers/iframe.html'


def calc_a_year(d):
    if d.month == 11:
        return date(d.year - 1, 12, 1)
    else:
        new_month = (d.month - 11) % 12
        new_year = d.year - 1 + (d.month / 12)
        return date(new_year, new_month, 1)


class CompanyView(DetailView):
    template_name = 'shirkers/details.html'
    model = Company
    slug_field = 'vat_id'
    slug_url_kwarg = 'vat_id'

    def get_missed_months(self, company):
        months = MissedMonths.objects.filter(
            company=company).values_list('missed_date')
        return {m[0] for m in months}

    def get_context_data(self, **kwargs):
        ctx = {
            'object': kwargs.get('object'),
        }
        if ctx['object']:
            start_date = settings.DATA_START_DATE
            end_date = MissedMonths.objects.all().aggregate(
                Max('missed_date'))['missed_date__max']
            missed_months = self.get_missed_months(ctx['object'])
            table_data = calc_table_data(start_date, end_date, missed_months)
            ctx['table_data'] = table_data
            ctx['missed_dates'] = len(missed_months) > 0
        return ctx

    def get_object(self, queryset=None):
        try:
            slug = self.kwargs.get(self.slug_url_kwarg)
            return Company.objects.filter(vat_id=slug).order_by('-id').first()
        except:  # Does not exist =>
            return None


class EmbedResult(CompanyView):
    template_name = 'shirkers/result.html'


class FindEmbedResult(CompanyView):
    template_name = 'shirkers/result.html'
    slug_field = 'name'
    slug_url_kwarg = 'name'

    def get_object(self, queryset=None):
        try:
            slug = self.kwargs.get(self.slug_url_kwarg)
            return Company.objects.filter(name=slug).order_by('-id').first()
        except:  # Does not exist =>
            return None
