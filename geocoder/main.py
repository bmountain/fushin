import my_geocoder
import uvicorn
from data_model import GeoData
from fastapi import FastAPI

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
    return my_geocoder.get_geodata(address)

if __name__ == '__main__':
    uvicorn.run('main:app', port=5000, reload=True)