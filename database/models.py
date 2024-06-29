from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import bcrypt
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

class Grievance(Base):
    __tablename__ = 'grievances'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, default="Pending")

    user = relationship("User", back_populates="grievances")

class Thread(Base):
    __tablename__ = 'threads'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User')

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    thread_id = Column(Integer, ForeignKey('threads.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    thread = relationship('Thread', back_populates='messages')
    user = relationship('User')

Thread.messages = relationship('Message', order_by=Message.id, back_populates='thread')

User.grievances = relationship("Grievance", order_by=Grievance.id, back_populates="user")

engine = create_engine('sqlite:///grievances.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Add an admin user if it does not exist
admin_username = "admin"
admin_password = "adminpass"
hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())

if not session.query(User).filter_by(username=admin_username).first():
    admin_user = User(username=admin_username, password=hashed_password, role="admin")
    session.add(admin_user)
    session.commit()
