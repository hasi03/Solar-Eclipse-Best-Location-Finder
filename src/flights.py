# Install the Python library from https://pypi.org/project/amadeus
from amadeus import Client, ResponseError
import numpy as np


def get_flight_price(key, secret, home_airport, destination, departure_date='2024-04-07'):
    amadeus = Client(
        client_id=key,
        client_secret=secret
    )

    try:
        '''
        Find the cheapest flights from home airport to destination on the specified departure date
        '''
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=home_airport, destinationLocationCode=destination, departureDate=departure_date, adults=1)
        
        price_count = len(response.data)

        prices = [response.data[i]['price']['total'] for i in range(price_count)]
        prices_array = np.array(prices, dtype=np.float64)
        if prices_array.size == 0:
            return None
        return prices_array.min() # Return the minimum price in Euro

    except ResponseError as error:
        raise error
