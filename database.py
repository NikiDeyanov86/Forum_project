from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import platform

if platform.system() == 'Linux': 
    engine = create_engine('sqlite:////test.db', convert_unicode=True)
elif platform.system() == 'Windows':
    engine = create_engine('sqlite:///test.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)
