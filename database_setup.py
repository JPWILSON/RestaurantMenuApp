import os
import sys

from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Restaurant(Base):
	__tablename__ = 'restaurant'
	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)

class MenuItem(Base):
	__tablename__ = 'menu_item'
	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)
	course = Column(String(50))
	description = Column(String(250))
	price = Column(String(10)) 
	restaurant_id = Column(ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)

#This is a decorator method, used for the JSON requests
	@property 
	def serialize(self):
		#Returns object data in easily serializable format
		return{
			'name'	:	self.name,
			'description'	:	self.description,
			'id'	:	self.id,
			'price'	:	self.price,
			'course'	:	self.course,
		}

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
