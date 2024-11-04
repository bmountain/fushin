from pydantic import BaseModel

class GeoData(BaseModel):
        fullname: str
        lon: float
        lat: float
        level: int