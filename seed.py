
from datetime import datetime
from sqlmodel import Session

from .database import create_db_and_tables, engine
from .models import User


def create_users():
    user_1 = User(
        name='Jhon Doe', 
        email='jhon.doe@gmail.com', 
        date_of_birth=datetime.now(), 
        height=175, 
        weight=70
    )

    with Session(engine) as session:  
        session.add(user_1)
        session.commit()  


def main():  
    create_db_and_tables()  
    create_users()  


if __name__ == "__main__":  
    main()  
