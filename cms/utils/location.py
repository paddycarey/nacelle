def parse_location_headers(headers):
    return {
        'country': headers.get("X-AppEngine-Country"),
        'region': headers.get("X-AppEngine-Region"),
        'city': headers.get("X-AppEngine-City"),
        'coordinates': headers.get("X-AppEngine-CityLatLong")
    }
