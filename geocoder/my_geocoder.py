import jageocoder
from data_model import GeoData


def get_geodata(address: str) -> GeoData:
    """
    Returns a geo-data of a given address in Japan. 

    Args:
        address (str): An address in Japan.

    Returns:
        GeoData: Fullname, longitude, latitude, and level of the address.
    """
    jageocoder.init()
    data = jageocoder.search(address)['candidates'][0]
    fullname: str = ''.join(data['fullname'])
    lon: float = data['x']
    lat: float = data['y']
    level: int = data['level']
    result = GeoData.model_validate({
        'fullname': fullname,
        'lon': lon,
        'lat': lat,
        'level': level
    })
    return result