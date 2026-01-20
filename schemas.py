from pydantic import BaseModel
class URLCreate(BaseModel):
    url: str
class URLInfo(BaseModel):
    original_url: str
    short_key: str
    clicks: int

    class Config:
        from_attributes = True  