import sys
from sqlalchemy import Column, Foreignkey, Integer, String
from sqlalchemy.ext.declaritive import declaritive_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declaritive_base()


engine = create_engine('sqlite://tournament.db')
Base.metadata.create_all(engine)
