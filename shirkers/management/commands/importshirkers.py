from django.core.management.base import BaseCommand, CommandError
from shirkers.helpers import fetch, parse, FetchError, ParseError
from shirkers.models import Company


class Command(BaseCommand):
    help = '''
Import companies that have not paid employee taxes.

Already imported entries will not be imported again.
    '''

    def handle(self, *args, **options):
        try:
            metadata, shirkers = parse(fetch())
        except FetchError:
            raise CommandError('An error happened while fetching new data.')
        except ParseError:
            raise CommandError('An error happened while parsing data.')

        # Don't do anything if there are already entries with same date in DB
        if Company.objects.filter(missed_date=metadata['ondate']).count():
            self.stdout.write(self.style.NOTICE(
                'Database already contains entries for this date!'))
        else:
            for company in shirkers:
                Company.objects.create(
                    vat_id=company['id'],
                    name=company['name'],
                    street=company['address']['street'],
                    postcode=company['address']['postcode'],
                    city=company['address']['city'],
                    missed_date=metadata['ondate']
                )
            self.stdout.write(self.style.SUCCESS(
                'Imported {} entries.'.format(len(shirkers))))
