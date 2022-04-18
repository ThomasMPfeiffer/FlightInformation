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
from .forms import *
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

    if request.POST.get('NonStopp'):
        kwargs= {'nonStop': 'true', **kwargs}  
    if  request.POST.get('IncludeAirlines'):
        kwargs= {'includedAirlineCodes': request.POST.get('IncludeAirlines'), **kwargs} 
    if request.POST.get('ExcludeAirlines'):
        kwargs= {'excludedAirlineCodes': request.POST.get('ExcludeAirlines'), **kwargs} 

    try: 
        offerresponse = amadeus.shopping.flight_offers_search.get(
        **kwargs)    
        #form = OfferserchResult(request.POST)
#        seatmap = {
#            "data": [
#                offerresponse.data[000]
#                ]
#            }
       # json_seatmap = json.dump(seatmap)
       
#        seatmapresponse = amadeus.shopping.seatmaps.post(seatmap)
#        seatmapresult = seatmapresponse.body  

    except ResponseError as error: 
        print(error) 
        messages.add_message(request, messages.ERROR, error) 
        return render(request, 'app/offersearch.html', {}) 

    #list with all the offers given to the formset
    offers = []

    
    for offer in offerresponse.data: 
        duration = offer['itineraries'][0]['duration']
        departureat = offer['itineraries'][0]['segments'][0]['departure']['at']
        departureiatacode = offer['itineraries'][0]['segments'][0]['departure']['iataCode']
        arrivalat = offer['itineraries'][0]['segments'][0]['arrival']['at']
        arrivaliatacode = offer['itineraries'][0]['segments'][0]['arrival']['iataCode']
        numberOfStops = offer['itineraries'][0]['segments'][0]['numberOfStops']
        carriercode = offer['itineraries'][0]['segments'][0]['carrierCode']
        flightnumber = offer['itineraries'][0]['segments'][0]['number']

        #flight = {'duration':  duration, 'departure': departureat, 'departureiataCode': departureiatacode, 'arrivalat': arrivalat, 'arrivaliataCode': arrivaliatacode, 'stops': numberOfStops, 'carrierCode': carriercode, 'flightnumber': flightnumber}

        durationRet= offer['itineraries'][1]['duration']
        departureatRet = offer['itineraries'][1]['segments'][0]['departure']['at']
        departureiatacodeRet = offer['itineraries'][1]['segments'][0]['departure']['iataCode']
        arrivalatRet = offer['itineraries'][1]['segments'][0]['arrival']['at']
        arrivaliatacodeRet = offer['itineraries'][1]['segments'][0]['arrival']['iataCode']
        numberOfStopsRet = offer['itineraries'][1]['segments'][0]['numberOfStops']
        carriercodeRet = offer['itineraries'][1]['segments'][0]['carrierCode']
        flightnumberRet = offer['itineraries'][1]['segments'][0]['number']

        #returnflight = {'durationret':  durationRet, 'departureret': departureatRet, 'departureiataCoderet': departureiatacodeRet, 'arrivalatret': arrivalatRet, 'arrivaliataCoderet': arrivaliatacodeRet, 'stopsret': numberOfStopsRet, 'carrierCoderet': carriercodeRet, 'flightnumberret': flightnumberRet}

        #price = {'price':offer['price']['total'],'currency': offer['price']['currency']}
        offer = {
            'duration':  duration, 'departure': departureat, 'departureiataCode': departureiatacode, 'arrivalat': arrivalat, 'arrivaliataCode': arrivaliatacode, 'stops': numberOfStops, 'carrierCode': carriercode, 'flightnumber': flightnumber,
            'durationret':  durationRet, 'departureret': departureatRet, 'departureiataCoderet': departureiatacodeRet, 'arrivalatret': arrivalatRet, 'arrivaliataCoderet': arrivaliatacodeRet, 'stopsret': numberOfStopsRet, 'carrierCoderet': carriercodeRet, 'flightnumberret': flightnumberRet,
            'price':offer['price']['total'],'currency': offer['price']['currency']
            }

        offers.append(offer)
        
    OffersearchResultFormSet = formset_factory(OfferseachResult, extra = 0)  
     
    offerformset = OffersearchResultFormSet(initial = offers)

    return render(request, "app/offersearch.html", {'offerformset': offerformset})




def availsearch(request):

    #dynamic json creation

    apidata= {}
    originDestinations = [{}]
    departureDateTime = {}
    originDestinations[0]['id'] = '1'
    originDestinations[0]['originLocationCode'] = request.POST.get('Origin')
    originDestinations[0]['destinationLocationCode'] = request.POST.get('Destination')
    departureDateTime['date'] = request.POST.get('Departuredate')
    originDestinations[0]['departureDateTime'] = departureDateTime
    apidata['originDestinations'] = originDestinations
    
    travelers = [{}]
    travelers[0]['id'] = '1'
    travelers[0]['travelerType'] = 'ADULT'
    apidata['travelers'] = travelers

    sources = ['GDS']
    apidata['sources'] = sources

    searchCriteria = {}
    flightFilters = {}
    carrierRestrictions = {}
    connectionRestriction = {}
    cabinRestrictions = [{}]

    if request.POST.get('Economy'):
        cabinRestrictions[0]['cabin'] = 'ECONOMY'
        cabinRestrictions[0]['originDestinationIds']=[1]
        flightFilters['cabinRestrictions']=cabinRestrictions
    if request.POST.get('PremEconomy'):
        cabinRestrictions[0]['cabin']='PREMIUM_ECONOMY'
        cabinRestrictions[0]['originDestinationIds']=[1]
        flightFilters[0]['cabinRestrictions']=cabinRestrictions
    if request.POST.get('Buisness'):
        cabinRestrictions[0]['cabin']='BUSINESS'
        cabinRestrictions[0]['originDestinationIds']=[1]
        flightFilters['cabinRestrictions']=cabinRestrictions
    if request.POST.get('First'):
        cabinRestrictions[0]['cabin']='FIRST'
        cabinRestrictions[0]['originDestinationIds']=[1]
        flightFilters['cabinRestrictions']=cabinRestrictions


    if request.POST.get('IncludedConnectionPoints'):
        includedConnectionPoints = request.POST.get('IncludedConnectionPoints').split(",")
        originDestinations[0]['includedConnectionPoints'] = includedConnectionPoints
    if  request.POST.get('ExcludedConnectionPoints'):
        excludedConnectionPoints = request.POST.get('ExcludedConnectionPoints').split(",")
        originDestinations[0]['excludedConnectionPoints'] = excludedConnectionPoints

    if request.POST.get('IncludeAirlines'):
        includedCarrierCodes = request.POST.get('IncludeAirlines').split(",")
        carrierRestrictions['includedCarrierCodes'] = includedCarrierCodes
        flightFilters['carrierRestrictions'] = carrierRestrictions
        
    if  request.POST.get('ExcludeAirlines'):
        excludedCarrierCodes = request.POST.get('ExcludeAirlines').split(",")
        carrierRestrictions['excludedCarrierCodes'] = excludedCarrierCodes
        flightFilters['carrierRestrictions']=carrierRestrictions

    if  request.POST.get('MaxStops'):
        maxNumberOfConnections = request.POST.get('MaxStops')
        connectionRestriction['maxNumberOfConnections'] = maxNumberOfConnections
        flightFilters['connectionRestriction'] = connectionRestriction

    searchCriteria['flightFilters']=flightFilters
    apidata['searchCriteria']= searchCriteria

    
    json_apidata = json.dumps(apidata)

    try: 
        response = amadeus.shopping.availability.flight_availabilities.post(
        json_apidata)
        responsehtml = response.body;
             
    except ResponseError as error: 
        print(error) 
        messages.add_message(request, messages.ERROR, error) 
      #  return render(request, 'app/availsearch.html', {}) 
    return render(request, "app/availsearch.html", {"availsearch": json_apidata})


def flightsearch(request):
    flightnumber =  request.POST.get('Flightnumber')
    if flightnumber:
        carrierCode = flightnumber[:2]
        number = flightnumber[2:]
        kwargs = {'carrierCode': carrierCode, 
                'flightNumber': number, 
                'scheduledDepartureDate': request.POST.get('ScheduledDepartureDate')}

        try: 
            statusresponse = amadeus.schedule.flights.get(
            **kwargs) 
        
            statusresult = statusresponse.body;
        except ResponseError as error: 
            print(error) 
            messages.add_message(request, messages.ERROR, error) 
            return render(request, 'app/flightsearch.html', {}) 
    else:
         return render(request, 'app/flightsearch.html', {}) 
    return render(request, "app/flightsearch.html", {"flightsearch": statusresult})










