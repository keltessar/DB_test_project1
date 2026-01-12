
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True, name ="Id")
    name = Column(String(50), unique=True, name = "Name")
    surname = Column(String(50), unique=True, name = "Surname")
    country = Column(String(50), unique=True, name = "Country")

# Экспортируем ВСЕ модели (если раскоментить модель выше - надо добавить ее в all ниже, через запятую)
__all__ = ['Base', 'User']