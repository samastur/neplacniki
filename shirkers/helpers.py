from datetime import date
import pendulum
import requests
from xml.etree import ElementTree

DATA_URL = 'http://seznami.gov.si/DURS/Nepredlagatelji.xml'
'''
Structure:
    Nepredlagatelji
        - Nepredlagatelji
            - Zavezanec (VAT ID): str (int)
            - Naziv (name): unicode
            - Naslov (address): unicode
        - Podatki
            - Dolg_na_dan (debt on date): ISO date
            - Pripravljeno (created): ISO date
'''


class FetchError(Exception):
    pass


class ParseError(Exception):
    pass


def calc_last_month(d):
    if d.month > 1:
        return date(d.year, d.month-1, 1)
    else:
        return date(d.year-1, 12, 1)


def next_month(d):
    if d.month < 12:
        return date(d.year, d.month + 1, 1)
    else:
        return date(d.year + 1, 1, 1)


def calc_table_data(start_date, end_date, fail_set):
    mon = []
    years = []

    start_year = start_date.year
    left_pad = [None] * (start_date.month - 1)
    right_pad = [None] * (12 - end_date.month)

    m = start_date
    while m <= end_date:
        mon.append(m not in fail_set)
        m = next_month(m)
    months = left_pad + mon + right_pad

    year = start_year
    while months:
        years.append({
            'year': year,
            'months': months[:12]
        })
        months = months[12:]
        year += 1
    years.reverse()  # Reverse order so freshest data (this year) is on top
    return years


def parse_xml(content):
    try:
        tree = ElementTree.fromstring(content)
    except:
        raise ParseError('Could not parse fetched data.')
    return tree


def fetch(url=DATA_URL):
    r = requests.get(url)
    if r.status_code != 200:
        raise FetchError('Problems with fetching data. HTTP code: ' +
                         str(r.status_code))
    tree = parse_xml(r.content)
    return tree


def local_fetch(filepath):
    tree = None
    with open(filepath, 'r') as f:
        tree = parse_xml(f.read())
    return tree


def parse(root):
    '''
    Parse XML into Python friendlier format.
    '''
    metaroot = root.find('Podatki')
    metadata = {
        'created': pendulum.parse(metaroot.find('Pripravljeno').text),
        'ondate': pendulum.parse(metaroot.find('Dolg_na_dan').text)
    }

    data = []
    for n in root.iterfind('Nepredlagatelji'):
        data.append({
            'id': n.find('Zavezanec').text,
            'name': unicode(n.find('Naziv').text),
            'address': parse_address(unicode(n.find('Naslov').text))
        })

    return [metadata, data]


def parse_address(address):
    street, zipcity = address.rsplit(', ', 1)
    zipcode, city = zipcity.split(' ', 1)
    return {
        'street': street,
        'postcode': int(zipcode),
        'city': city
    }
