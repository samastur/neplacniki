from datetime import date
import json

from django.views.generic import DetailView, TemplateView

from .models import Company, MissedMonths


class Home(TemplateView):
    template_name = 'shirkers/index.html'

    @staticmethod
    def find_companies(query):
        try:
            int(query)  # Checks if query is a number
            filtered = Company.objects.filter(
                vat_id__contains=query).distinct()
        except:
            filtered = Company.objects.filter(
                name__icontains=query).distinct()
        return filtered

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        companies = []
        if request.GET.get('q', None):
            question = request.GET.get('q', '')
            companies = Home.find_companies(question)

        if len(companies) > 1:
            ctx['companies'] = companies
            ctx['matches'] = json.dumps([
                {'id': x.vat_id, 'name': x.name} for x in companies
            ])
            return self.render_to_response(ctx)
        return self.render_to_response(ctx)


def calc_last_month(d):
    if d.month > 1:
        return date(d.year, d.month-1, 1)
    else:
        return date(d.year-1, 12, 1)


def calc_month_difference(d1, d2):
    return (d1.month - d2.month) % 12 + (d1.year - d2.year)


def is_same_month(d1, d2):
    return d1.year == d2.year and d1.month == d2.month


class CompanyView(DetailView):
    template_name = 'shirkers/details.html'
    model = Company
    slug_field = 'vat_id'
    slug_url_kwarg = 'vat_id'

    def filter_from_date(self, faults, from_date):
        prev_month = calc_last_month(from_date)
        filtered = []
        for fault in faults:
            month_diff = calc_month_difference(prev_month, fault.missed_date)
            if month_diff <= 12:
                filtered.append(fault)
        return filtered

    def get_context_data(self, **kwargs):
        ctx = {
            'object': kwargs['object']
        }
        if ctx['object']:
            faults = MissedMonths.objects.filter(
                company=ctx['object']).order_by(
                    '-missed_date').only('missed_date')[:12]
            ctx['faults'] = self.filter_from_date(faults, date.today())
            ctx['missed_dates'] = [x.missed_date for x in faults]
        return ctx

    def get_object(self, queryset=None):
        try:
            slug = self.kwargs.get(self.slug_url_kwarg)
            return Company.objects.filter(vat_id=slug).order_by('-id').first()
        except:  # Does not exist =>
            return None
