from pydantic import BaseModel, validator
from models.enums import ResponseEnum
from typing import Optional

class IMEIResponse(BaseModel):
    imei: str


class IMEIService(BaseModel):
    id: int
    title: str

class IMEIResponseProperties(BaseModel):
    deviceName: str = None
    image: str = None
    serial: str = None
    estPurchaseDate: int = None
    gsmaBlacklisted: bool = None
    simLock: bool = None
    replaced: bool = None
    warrantyStatus: str = None
    technicalSupport: bool = None
    modelDesc: str = None
    demoUnit: bool = None
    purchaseCountry: str = None
    loaner: bool = None
    fmiOn: bool = None
    lostMode: bool = None
    usaBlockStatus: str = None

class IMEIResponseParsed(BaseModel):
    id: str
    type: str
    status: ResponseEnum
    orderId: Optional[str] = None
    service: IMEIService
    amount: str
    deviceId: str
    processedAt: int
    properties: Optional[IMEIResponseProperties] = None

    class Config:
        extra = "ignore"  # Игнорируем дополнительные поля (например, "!!! WARNING !!!")

    @validator('properties', pre=True)
    def empty_list_to_none(cls, v):
        if isinstance(v, list) and not v:
            return None
        return v