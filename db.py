from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://ilyava:1qaz2wsx@127.0.0.1:5432/flask_home_work')
Session = sessionmaker(bind=engine)  # создание сессии