"""
Definition of forms.
"""

from django import forms
from django.forms import formset_factory
from django.contrib.auth.forms import AuthenticationForm
from django.forms.models import BaseInlineFormSet
from django.forms.models import inlineformset_factory
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


class Offersearch_Segment(forms.Form):
    departure = forms.CharField(disabled = True)
    departureiataCode = forms.CharField(disabled = True)
    arrivalat = forms.CharField(disabled = True)
    arrivaliataCode = forms.CharField(disabled = True)
    stops = forms.IntegerField(disabled = True)
    carrierCode = forms.CharField(disabled = True)
    flightnumber = forms.IntegerField(disabled = True)


segments_FormSet = formset_factory(Offersearch_Segment, extra = 0)



class FlightSearch_flightpoints(forms.Form):
    iataCode = forms.CharField(disabled = True)

flightpoints_FormSet = formset_factory(FlightSearch_flightpoints, extra = 0)

class FlightSearch_legs(forms.Form):
    aircraftType = forms.CharField(disabled = True)
    scheduledLegDuration = forms.CharField(disabled = True)

legs_FormSet = formset_factory(FlightSearch_legs, extra = 0)