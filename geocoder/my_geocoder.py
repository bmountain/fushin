import jageocoder
from data_model import GeoData


class GeoCodingException(Exception):
    pass

def get_geodata(address: str) -> GeoData:
    """
    与えられた住所の地理空間データを返す

    Args:
        address (str): 日本の住所

    Returns:
        GeoData: 地名、経度、緯度、住所レベル
    """
    try:
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
    except:
        raise GeoCodingException