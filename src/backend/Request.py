from amadeus import Client
from src.backend.utils import geocode_city
amadeus = Client(
    client_id='ihBJLkd2SDQFIp7MvlHDcAExAFaBiN1n',
    client_secret='XJ2JSLSG0bL5Mky6'
)

class Request(object):
    def __init__(self, current_city = 'NONE', travel_city = 'NONE', ratings = 'NONE', num_people = '1', st_date = 'NONE', end_date = 'NONE',max_fbudget = 'NONE', max_hbudget = 'NONE', currency = 'USD'):
        self.current = current_city
        self.travel = travel_city
        self.ratings = ratings
        self.num_people = num_people
        self.st_date = st_date
        self.end_date = end_date
        self.max_hbudget = max_hbudget
        self.currency = currency
        self.max_fbudget = max_fbudget

    def get_hotels(self):
        lat, long = geocode_city(self.travel)
        request = amadeus.reference_data.locations.airports.get(
            latitude=lat,
            longitude=long
        )
        self.travel = request.data[0]['address']['cityCode']
        request = amadeus.shopping.hotel_offers.get(
            cityCode= self.travel,
            checkInDate = self.st_date,
            checkOutDate = self.end_date,
            currency = self.currency,
            adults = self.num_people,
            ratings= self.ratings,
            radius = 20,
            priceRange = self.max_hbudget
        )
        return request.data
    def get_flight(self):
        request = amadeus.shopping.flight_offers.get(
            origin = self.current,
            destination = self.travel,
            departureDate = self.st_date,
            returnDate = self.end_date,
            adults = self.num_people,
            currency = self.currency,
            maxPrice = self.max_fbudget
        )
        return request.data
    def get_nearby_airports(self):
        lat, long = geocode_city(self.current)
        request = amadeus.reference_data.locations.airports.get(
            latitude = lat,
            longitude = long
        )
        return [request.data[i]['iataCode'] for i in range(len(request.data))]
req = Request(current_city='Chicago', travel_city='New York City', num_people='2', st_date='2019-03-16', end_date='2019-03-20', ratings='5,4,3,2', max_fbudget='300')

print(req.get_hotels())
