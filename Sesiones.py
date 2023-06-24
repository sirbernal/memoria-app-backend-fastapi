from pydantic import BaseModel


class Sesion(BaseModel):
    user_id: int
    trainer_id: int
    title: str
    description: str
    sessions_url: str
    training_details: str