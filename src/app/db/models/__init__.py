from sqlalchemy import Column, DateTime, String, ForeignKey, Integer, Enum
from sqlalchemy.orm import declarative_base, relationship
from app.schemas import SystemItemType

Base = declarative_base()


class Items(Base):
    __tablename__ = 'items'

    id = Column(String, primary_key=True)
    url = Column(String, nullable=True)
    date = Column(DateTime, nullable=False)
    parentId = Column(String, ForeignKey("items.id", ondelete='CASCADE'), nullable=True)
    type = Column(Enum(SystemItemType), nullable=False)
    size = Column(Integer, nullable=True)
    children = relationship('Items', cascade='all, delete-orphan')
