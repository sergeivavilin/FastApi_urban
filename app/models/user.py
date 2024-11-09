from sqlalchemy import Integer, String, Column, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.backend.db import Base


class User(Base):
    __tablename__ = "users"
    ___table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    slug = Column(String, unique=True, index=True)
    tasks  = relationship("Task", back_populates="user")


if __name__ == "__main__":

    from sqlalchemy.schema import CreateTable
    print(CreateTable(User.__table__))
