from datetime import date
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView, TemplateView

from .models import Company, MissedMonths


class Home(TemplateView):
    template_name = 'shirkers/index.html'
    num_hits = 10

    def find_companies(self, query):
        print query
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

        if len(companies) > 1:
            if request.GET.get('format') == 'json':
                matches = json.dumps([
                    {'id': x.vat_id, 'value': x.name} for x in companies
                ])
                return HttpResponse(matches, content_type='application/json')
            else:
                ctx['companies'] = companies
        elif len(companies) == 1:
            return HttpResponseRedirect(companies[0].get_absolute_url())
        return self.render_to_response(ctx)


def calc_last_month(d):
    if d.month > 1:
        return date(d.year, d.month-1, 1)
    else:
        return date(d.year-1, 12, 1)


def calc_a_year(d):
    if d.month == 12:
        return date(d.year, 1, 1)
    else:
        return date(d.year-1, (d.month-11) % 12, 1)


class CompanyView(DetailView):
    template_name = 'shirkers/details.html'
    model = Company
    slug_field = 'vat_id'
    slug_url_kwarg = 'vat_id'
    num_months = 12

    def get_context_data(self, **kwargs):
        ctx = {
            'object': kwargs['object']
        }
        if ctx['object']:
            prev_month = calc_last_month(date.today())
            period_start = calc_a_year(prev_month)
            faults = MissedMonths.objects.filter(
                company=ctx['object'],
                missed_date__gte=period_start).order_by(
                    '-missed_date').only('missed_date')
            ctx['faults'] = list(faults)
            ctx['missed_dates'] = [x.missed_date for x in faults]
        return ctx

    def get_object(self, queryset=None):
        try:
            slug = self.kwargs.get(self.slug_url_kwarg)
            return Company.objects.filter(vat_id=slug).order_by('-id').first()
        except:  # Does not exist =>
            return None
