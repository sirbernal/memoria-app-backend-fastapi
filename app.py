from bson import ObjectId
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from User import User, Base
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing_extensions import Annotated
from pymongo import MongoClient
from Sesiones import Sesion
import os

app = FastAPI()


MONGO_URL = os.environ.get('MONGODB_URL', 'mongodb://localhost:27017/')
POSTGRES_URL = os.environ.get('POSTGRES_URL', 'postgresql://postgres:postgres@localhost:5432/users')

# Conexión a la base de datos
engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Conectarse a MongoDB
client = MongoClient(MONGO_URL)
db = client["sesiones"]

# Obtener la colección "sesiones"
sesiones = db["sessions"]


origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/login")
#def login(form_data: OAuth2PasswordRequestForm = Depends()):
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=form_data.username).first()
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(status_code=403, detail="Incorrect username or password")
    if user.user_type == "user":
        token = {"user": user.username, 'user_type': user.user_type, 'user_id': user.id, 'associate_trainer': user.associate_trainer }
    elif user.user_type == "trainer":
        token = {"user": user.username, 'user_type': user.user_type, 'trainer_id': user.id, 'associate_user': user.associate_user }
    return token

# Definir ruta para obtener todas las sesiones
@app.get("/sesiones/{id_usuario}/{id_entrenador}")
async def get_sesiones(id_usuario: int, id_entrenador: int):
    result = []
    for sesion in sesiones.find():
        #sesion.pop('_id', None)
        sesion['_id'] = str(sesion['_id'])
        if id_usuario == sesion["user_id"] and id_entrenador == sesion["trainer_id"]:
            result.append(sesion)
    return result


@app.put("/sesiones/{sesion_id}")
async def update_sesion(sesion_id: str, sesion: Sesion):
    obj_id = ObjectId(sesion_id)
    result = sesiones.update_one({'_id': obj_id}, {'$set': sesion.dict()})

    if result.modified_count == 1:
        return {"id": str(sesion_id)}
    elif result.modified_count == 0 and result.matched_count == 1:
        return {"id": 0}
    else:
        raise HTTPException(status_code=500, detail="Error al insertar el objeto en la base de datos")

@app.post("/sesiones/")
async def create_sesion(sesion: Sesion):
    sesion_dict = sesion.dict()
    result = sesiones.insert_one(sesion_dict)
    return {"id": str(result.inserted_id)}

@app.delete("/sesiones/{sesion_id}")
async def create_sesion(sesion_id: str):
    obj_id = ObjectId(sesion_id)
    result = sesiones.delete_one({'_id': obj_id})
    return {"deleted_count": result.deleted_count}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)