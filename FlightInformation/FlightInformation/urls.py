"""
Definition of urls for FlightInformation.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views


urlpatterns = [

    url(r'^$', app.views.home, name='home'),
    url(r'^offersearch$', app.views.offersearch, name='offersearch'),
    url(r'^availsearch$', app.views.availsearch, name='availsearch'),

]
