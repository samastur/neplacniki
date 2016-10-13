from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models


class Company(models.Model):
    vat_id = models.CharField(max_length=8, db_index=True)
    name = models.TextField(db_index=True)
    street = models.CharField(max_length=128)
    postcode = models.SmallIntegerField()
    city = models.CharField(max_length=128)

    def get_absolute_url(self):
        return reverse('company_view', args=[self.vat_id])


class MissedMonths(models.Model):
    company = models.ForeignKey(Company)
    missed_date = models.DateField()
