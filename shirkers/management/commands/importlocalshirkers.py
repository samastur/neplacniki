from .importshirkers import Command as ShirkerCommand
from shirkers.helpers import local_fetch


class Command(ShirkerCommand):
    args = '<xml_filepath>'
    help = '''
Import companies that have not paid employee taxes.

Already imported entries will not be imported again.
    '''

    def fetch(self, address):
        return local_fetch(address)

    def handle(self, *args, **options):
        for path in args:
            self.stdout.write(self.style.SUCCESS(
                'Importing {}....'.format(path)))
            self.import_data(path)
