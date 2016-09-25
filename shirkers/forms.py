# -*- coding: utf-8 -*-
from django import forms


class SearchCompany(forms.Form):
    q = forms.CharField(
        help_text=u'Vnesite ime podjetja ali njegovo davčno številko',
        strip=True
    )
