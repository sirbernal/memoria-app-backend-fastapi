from pydantic import BaseModel

class TrainerContact(BaseModel):
    cover_img: str
    meta_img: str
    name: str
    short_description: str
    number: str
    email: str
    full_description: str
    socials: dict