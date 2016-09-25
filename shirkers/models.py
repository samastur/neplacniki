from __future__ import unicode_literals

from django.db import models


class Company(models.Model):
    vat_id = models.CharField(max_length=8, db_index=True)
    name = models.TextField(db_index=True)
    street = models.CharField(max_length=128)
    postcode = models.SmallIntegerField()
    city = models.CharField(max_length=128)
    missed_date = models.DateField()
