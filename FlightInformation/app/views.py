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
        offerresponse = amadeus.shopping.flight_offers_search.get(
        **kwargs)
        seatmap = {
            "data": [
                offerresponse.data[000]
                ]
            }
       # json_seatmap = json.dump(seatmap)
       
        seatmapresponse = amadeus.shopping.seatmaps.post(seatmap)
        result = seatmapresponse.body    
    except ResponseError as error: 
        print(error) 
        messages.add_message(request, messages.ERROR, error) 
        return render(request, 'app/offersearch.html', {}) 
    return render(request, "app/offersearch.html", {"offersearch": result})



def availsearch(request):
   
    kwargs = {
    "originDestinations": [
     {
         "id": "1",
         "originLocationCode": request.POST.get('Origin'),
         "destinationLocationCode": request.POST.get('Destination'),
         "departureDateTime": 
         {
           "date": request.POST.get('Departuredate'),
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
    }  
    
    json_kwargs = json.dumps(kwargs)

    try: 
        response = amadeus.shopping.availability.flight_availabilities.post(
        json_kwargs)
             
    except ResponseError as error: 
        print(error) 
        messages.add_message(request, messages.ERROR, error) 
        return render(request, 'app/availsearch.html', {}) 
    return render(request, "app/availsearch.html", {"availsearch": response})












