import json

from django.views.generic import DetailView, TemplateView

from .models import Company


class Home(TemplateView):
    template_name = 'shirkers/index.html'

    @staticmethod
    def find_companies(query):
        try:
            int(query)  # Checks if query is a number
            filtered = Company.objects.filter(
                vat_id__contains=query).values('name', 'vat_id')
        except:
            filtered = Company.objects.filter(
                name__icontains=query).values('name', 'vat_id')
        return list(filtered)

    def get(self, request, *args, **kwargs):
        print 'home'
        ctx = self.get_context_data(**kwargs)
        companies = []
        if request.GET.get('q', None):
            question = request.GET.get('q', '')
            companies = Home.find_companies(question)

        if len(companies) > 1:
            print companies
            ctx['matches'] = json.dumps(companies)
            return self.render_to_response(ctx)
        return self.render_to_response(ctx)


class CompanyView(DetailView):
    template_name = 'shirkers/details.html'
    model = Company
    slug_field = 'vat_id'
    slug_url_kwarg = 'vat_id'

    def get_context_data(self, **kwargs):
        ctx = {
            'object': kwargs['object']
        }
        if ctx['object']:
            faults = Company.objects.filter(
                vat_id=ctx['object'].vat_id).values_list('missed_date')
            ctx['faults'] = [v[0] for v in faults]
        return ctx

    def get_object(self, queryset=None):
        try:
            return super(CompanyView, self).get_object(queryset)
        except:  # Does not exist =>
            return None
