"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http import HttpResponse
from amadeus import Client, ResponseError 
from django.contrib import messages 
import json

amadeus = Client(client_id='In8XtAGXlpWyURmQE3FQFSyGiUC3YSAL', 
                 client_secret='xwDB70qfB4AAnMrT', 
                 log_level='debug') 

def home(request):
    kwargs = {'originLocationCode': request.POST.get('Origin'), 
              'destinationLocationCode': request.POST.get('Destination'), 
              'departureDate': request.POST.get('Departuredate'), 
              'returnDate': request.POST.get('Returndate')} 
    try: 
        purpose = amadeus.travel.predictions.trip_purpose.get( 
            **kwargs).data['result'] 
    except ResponseError as error: 
        print(error) 
        messages.add_message(request, messages.ERROR, error) 
        return render(request, 'app/index.html', {}) 
    return render(request, 'app/index.html', {'prediction': purpose})    



def offersearch(request): 
    kwargs = {'originLocationCode': request.POST.get('Origin'), 
            'destinationLocationCode': request.POST.get('Destination'), 
            'departureDate': request.POST.get('Departuredate'), 
            'returnDate':  request.POST.get('Returndate'),
            'adults':  request.POST.get('Amount_adults'),
            'travelClass':  request.POST.get('Class')}
            
    try: 
        response = amadeus.shopping.flight_offers_search.get(
        **kwargs)
             
    except ResponseError as error: 
        print(error) 
        messages.add_message(request, messages.ERROR, error) 
        return render(request, 'app/offersearch.html', {}) 
    return render(request, "app/offersearch.html", {"offersearch": response})



def availsearch(request):
    kwargs = {'originLocationCode': request.POST.get('Origin'), 
            'destinationLocationCode': request.POST.get('Destination'), 
            'departureDate': request.POST.get('Departuredate')}
    json_kwargs = json.dumps(kwargs)
    teststring = """{
    "originDestinations": [
     {
         "id": "1",
         "originLocationCode": "BOS",
         "destinationLocationCode": "MAD",
        "departureDateTime": {
           "date": "2022-02-14",
           "time": "21:15:00"
             }
     }
     ],
    "travelers": [
      {
       "id": "1",
       "travelerType": "ADULT"
     }
     ],
    "sources": [
      "GDS"
     ]
    }"""  
    
    testjson = json.loads(teststring)

    try: 
        response = amadeus.shopping.availability.flight_availabilities.post(
        testjson)
             
    except ResponseError as error: 
        print(error) 
        messages.add_message(request, messages.ERROR, error) 
        return render(request, 'app/availsearch.html', {}) 
    return render(request, "app/availsearch.html", {"availsearch": response})



def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )




def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )










