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
        seatmap = {
           "data": [
               offerresponse.data[00]
               ]
            }
        json_seatmap = json.dumps(seatmap)
       
        seatmapresponse = amadeus.shopping.seatmaps.post(seatmap)
        seatmapresult = seatmapresponse.body  

    except ResponseError as error: 
        print(error) 
        messages.add_message(request, messages.ERROR, error) 
        return render(request, 'app/offersearch.html', {}) 

    #list with all the offers given to the formset
    offers = []
 
    for offer in offerresponse.data:

         #flight
        segments = []
        flights=len(offer['itineraries'][0]['segments'])
        flightsret= len(offer['itineraries'][1]['segments'])
        for segment in range(flights):             
            departureat = offer['itineraries'][0]['segments'][segment]['departure']['at']
            departureiatacode = offer['itineraries'][0]['segments'][segment]['departure']['iataCode']
            arrivalat = offer['itineraries'][0]['segments'][segment]['arrival']['at']
            arrivaliatacode = offer['itineraries'][0]['segments'][segment]['arrival']['iataCode']
            numberOfStops = offer['itineraries'][0]['segments'][segment]['numberOfStops']
            carriercode = offer['itineraries'][0]['segments'][segment]['carrierCode']
            flightnumber = offer['itineraries'][0]['segments'][segment]['number']

            segment = {'departure': departureat, 'departureiataCode': departureiatacode, 'arrivalat': arrivalat, 'arrivaliataCode': arrivaliatacode, 'stops': numberOfStops, 'carrierCode': carriercode, 'flightnumber': flightnumber}
            segments.append(segment)

        segmentsFormSetFlight = segments_FormSet(initial = segments)

        #returnflight
        segmentsret = []

        for segment in range(flightsret):     
            departureatRet = offer['itineraries'][1]['segments'][segment]['departure']['at']
            departureiatacodeRet = offer['itineraries'][1]['segments'][segment]['departure']['iataCode']
            arrivalatRet = offer['itineraries'][1]['segments'][segment]['arrival']['at']
            arrivaliatacodeRet = offer['itineraries'][1]['segments'][segment]['arrival']['iataCode']
            numberOfStopsRet = offer['itineraries'][1]['segments'][segment]['numberOfStops']
            carriercodeRet = offer['itineraries'][1]['segments'][segment]['carrierCode']
            flightnumberRet = offer['itineraries'][1]['segments'][segment]['number']

            returnsegment = {'departure': departureatRet, 'departureiataCode': departureiatacodeRet, 'arrivalat': arrivalatRet, 'arrivaliataCode': arrivaliatacodeRet, 'stops': numberOfStopsRet, 'carrierCode': carriercodeRet, 'flightnumber': flightnumberRet}
            segmentsret.append(returnsegment)
        
        segmentsFormSetRet = segments_FormSet(initial = segmentsret)


        duration = offer['itineraries'][0]['duration']
        durationRet= offer['itineraries'][1]['duration']
        price = {'price':offer['price']['total'],'currency': offer['price']['currency']}

        singleoffer = {'Duration':duration, 'Flight segments':segmentsFormSetFlight, 'Returnflight duration': durationRet, 'Returnflight segments': segmentsFormSetRet}
        singleoffer.update(price)

        offers.append(singleoffer)
        
   # OffersearchResultFormSet = formset_factory(Offersearch_Offer, extra = 0)  
     
   # offerformset = OffersearchResultFormSet(initial = offers)

    return render(request, "app/offersearch.html", {'offers': offers})


    


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
        responsejson = json.loads(responsehtml)
             
    except ResponseError as error: 
        print(error) 
        messages.add_message(request, messages.ERROR, error) 
        return render(request, 'app/availsearch.html', {})
    

    flights = []
    if 'data' in responsejson:       

        
        
        flightslen = len(responsejson['data'])
        for flight in range(flightslen):
            flightstring = ""
            segments= len(responsejson['data'][flight]['segments'])
            segmentslist = []
            for segment in range(segments):
                carrierCode = responsejson['data'][flight]['segments'][segment]['carrierCode']
                flightNumber = responsejson['data'][flight]['segments'][segment]['number']
                iataCodeDep = responsejson['data'][flight]['segments'][segment]['departure']['iataCode']
                iataCodeArrial = responsejson['data'][flight]['segments'][segment]['arrival']['iataCode']
                flightstring = carrierCode + flightNumber + " " + iataCodeDep + "-" + iataCodeArrial + " "  #Create Outputstring First Part               
                bookableClasses = len(responsejson['data'][flight]['segments'][segment]['availabilityClasses'])
                for bookableClass in range(bookableClasses):
                    seatclass = responsejson['data'][flight]['segments'][segment]['availabilityClasses'][bookableClass]['class']
                    numberOfBookableSeats = responsejson['data'][flight]['segments'][segment]['availabilityClasses'][bookableClass]['numberOfBookableSeats']
                    flightstring += (seatclass + str(numberOfBookableSeats) + " ")
                segmentslist.append(flightstring)
            flights.append(segmentslist)
    else:
        flights.append("There are no Flights available")

    return render(request, "app/availsearch.html", {"flights": flights})


def flightsearch(request):
    flightnumber =  request.POST.get('Flightnumber')
    if flightnumber:
        carrierCode = flightnumber[:2]
        number = flightnumber[2:]
        kwargs = {'carrierCode': carrierCode, 
                'flightNumber': int(number), 
                'scheduledDepartureDate': request.POST.get('ScheduledDepartureDate')}

        try: 
            statusresponse = amadeus.schedule.flights.get(
            **kwargs) 
        
        except ResponseError as error: 
            print(error) 
            messages.add_message(request, messages.ERROR, error) 
            return render(request, 'app/flightsearch.html', {}) 

        flights = []
        for dataset in statusresponse.data:            
            scheduledDepartureDate = dataset['scheduledDepartureDate']
            carrierCode = dataset['flightDesignator']['carrierCode']
            flightNumber = dataset['flightDesignator']['flightNumber']

            amountflightPoints = len(dataset['flightPoints'])
            flightpoints = []
            for flightpoint in range(amountflightPoints):
                iataCode = dataset['flightPoints'][flightpoint]['iataCode']
                if flightpoint == 0:
                    timingValue = dataset['flightPoints'][flightpoint]['departure']['timings'][0]['value']  
                if flightpoint == 1:
                    timingValue = dataset['flightPoints'][flightpoint]['arrival']['timings'][0]['value']  
                #timings ist eine Liste. Überprüfen, ob hier ggf mehrere Timings möglich sind und sind es immer zwei Flightpoints?? kann arrival und departure 0 und 1 sein?

                singleflightpoint ={'iataCode':iataCode, 'timingValue':timingValue}
                flightpoints.append(singleflightpoint)

            flightpointsFormSet = flightpoints_FormSet(initial = flightpoints)
            flight = {'scheduledDepartureDate':scheduledDepartureDate, 'carrierCode':carrierCode, 'flightNumber':flightNumber, 'flightpoints':flightpointsFormSet}
            flights.append(flight)

        if len(flights)==0:
           flights = "There are no flights available" 
    else:
         return render(request, 'app/flightsearch.html', {}) 
    return render(request, "app/flightsearch.html", {"flights": flights})


def seatmap(request):

        return render(request, "app/seatmap.html")
 





