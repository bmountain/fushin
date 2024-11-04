import my_geocoder
import uvicorn
from data_model import GeoData
from fastapi import FastAPI

# TODO: ジオコーディング失敗時にinternal server errorを投げる

class GeoCodingAPIException(Exception):
    pass

app = FastAPI()

@app.post('/')
async def geocoder(address: str) -> GeoData:
    """
    Returns a geo-data of a given address in Japan. 

    Args:
        address (str): An address in Japan.

    Returns:
        GeoData: Fullname, longitude, latitude, and level of the address.
    """
    try:
        return my_geocoder.get_geodata(address)
    except:
        raise GeoCodingAPIException


if __name__ == '__main__':
    uvicorn.run('main:app', port=5000, reload=True)