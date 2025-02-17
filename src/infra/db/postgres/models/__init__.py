import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr




class TimeStampMixin:

    @declared_attr
    def created_at(cls):
        return so.mapped_column(sa.DateTime, default=sa.func.now())
    
    @declared_attr
    def updated_at(cls):
        return so.mapped_column(sa.DateTime, default=sa.func.now(), onupdate=sa.func.now())
    
    
Base = declarative_base()



from .user import User
from .requests import Request

