from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from User import User, Base

import random

# Conexión a la base de datos
SQLALCHEMY_DATABASE_URL = 'postgresql://memoria-app-postgres.postgres.database.azure.com:5432/users?user=postgres&password=9onrsCJEVgQJ&sslmode=require'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Crear todas las tablas en la base de datos
Base.metadata.create_all(bind=engine)



# Crear un nuevo registro en la tabla de usuarios
db = SessionLocal()

for i in range(17,22):
    username = 'usuario' + str(i)
    user_type =  "user" if i % 2 == 0 else "trainer"
    numero = random.randint (1, 1000)
    password = 'pass' + str(numero)
    user = User()
    if user_type == "user":
        user = User(username=username, email= username + "@prueba.com", user_type=user_type, associate_trainer = i+2)
    else:
        user = User(username=username, email= username + "@prueba.com", user_type=user_type, associate_user = [i])
    user.set_password(password)
    db.add(user)
    db.commit()
    db.refresh(user)
    print("User created:", user.username + " -> " + user.user_type + "   PASSWORD: " + password)