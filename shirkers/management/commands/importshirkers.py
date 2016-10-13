from django.core.management.base import BaseCommand, CommandError
from shirkers.helpers import fetch, parse, FetchError, ParseError
from shirkers.models import Company, MissedMonths


class Command(BaseCommand):
    help = '''
Import companies that have not paid employee taxes.

Already imported entries will not be imported again.
    '''

    def fetch(self, address):
        return fetch()

    def import_data(self, address=None):
        try:
            metadata, shirkers = parse(self.fetch(address))
        except FetchError:
            raise CommandError('An error happened while fetching new data.')
        except ParseError:
            raise CommandError('An error happened while parsing data.')

        # Don't do anything if there are already entries with same date in DB
        if MissedMonths.objects.filter(missed_date=metadata['ondate']).count():
            self.stdout.write(self.style.NOTICE(
                'Database already contains entries for this date!'))
        else:
            for company in shirkers:
                # First create Company object, if it doesn't exist yet
                comp, created = Company.objects.get_or_create(
                    vat_id=company['id'],
                    defaults={
                        'name': company['name'],
                        'street': company['address']['street'],
                        'postcode': company['address']['postcode'],
                        'city': company['address']['city'],
                    })

                # Add missing date for it
                MissedMonths.objects.create(
                    company=comp,
                    missed_date=metadata['ondate'])
                '''
                Company.objects.create(
                    vat_id=company['id'],
                    name=company['name'],
                    street=company['address']['street'],
                    postcode=company['address']['postcode'],
                    city=company['address']['city'],
                    missed_date=metadata['ondate']
                )
                '''
            self.stdout.write(self.style.SUCCESS(
                'Imported {} entries.'.format(len(shirkers))))

    def handle(self, *args, **options):
        self.import_data()
