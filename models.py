from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func
from db import engine

Base = declarative_base(bind = engine)  #создает базовый класс для orm-моделей

class Adv(Base):
    __tablename__ = 'advertisments'  # указываем на какую таблицу ссылается класс
                                     # в джанго на базе класса таблица формируется автоматически
                                     # во фласке это требуется прописать вручную
    id = Column(Integer, primary_key=True, autoincrement=True)
    header = Column(String, nullable=False, unique=False)
    description = Column(String, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
    owner = Column(String, nullable=False)


Base.metadata.create_all()  # производит миграцию. если в базе нет какой-то таблицы - она создатся
                            # если менять поля выше, то эта функция не сработает