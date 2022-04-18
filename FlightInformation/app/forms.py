"""
Definition of forms.
"""

from django import forms
from django.forms import formset_factory
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

SELECT_FLIGHTCLASS = ["Economy", "Premium Economy", "Buisness", "First"]

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


#class offersearchForm(forms.Form):
class OfferseachResult(forms.Form):
    duration = forms.CharField(disabled = True)
    departure = forms.CharField(disabled = True)
    departureiataCode = forms.CharField(disabled = True)
    arrivalat = forms.CharField(disabled = True)
    arrivaliataCode = forms.CharField(disabled = True)
    stops = forms.IntegerField(disabled = True)
    carrierCode = forms.CharField(disabled = True)
    flightnumber = forms.IntegerField(disabled = True)

    durationret = forms.CharField(disabled = True)
    departureret = forms.DateField(disabled = True)
    departureiataCoderet = forms.CharField(disabled = True)
    arrivalatret = forms.DateField(disabled = True)
    arrivaliataCoderet = forms.CharField(disabled = True)
    stopsret = forms.IntegerField(disabled = True)
    carrierCoderet = forms.CharField(disabled = True)
    flightnumberret = forms.IntegerField(disabled = True)

    price = forms.CharField(disabled = True)
    currency = forms.CharField(disabled = True)


