from sqlalchemy import create_engine, Float, Column, Integer, String, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class EndOfDay(Base):
    __tablename__ = 'end_of_day'

    id = Column(Integer, primary_key=True)
    date = Column(String)
    clearing_number = Column(String)
    account = Column(String)
    margin_type = Column(String)
    margin = Column(Float)

    def __init__(self) -> None:
        super().__init__()

    def __repr__(self):
        return f"EndOfDay(date={self.date}, cleaning_number={self.cleaning_number}, account={self.account}, margin_type={self.margin_type}, margin={self.margin})"
    

class Intraday(Base):
    __tablename__ = 'intraday'

    id = Column(Integer, primary_key=True)
    date = Column(String)
    time = Column(String)
    clearing_number = Column(String)
    account = Column(String)
    margin_type = Column(String)
    margin = Column(Float)

    def __init__(self) -> None:
        super().__init__()

    def __repr__(self):
        return f"Intraday(date={self.date}, time={self.time}, cleaning_number={self.cleaning_number}, account={self.account}, margin_type={self.margin_type}, margin={self.margin})"



def get_session():
    engine = create_engine('sqlite:///LZDB.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def create_tables():
    session = get_session()
    engine = session.get_bind()
    # check if tables exist
    if not inspect(engine).has_table('end_of_day') and not inspect(engine).has_table('intraday'):
        # create tables
        Base.metadata.create_all(engine)
    
    insert_data()

def insert_data():
    session = get_session()
    if session.query(EndOfDay).count() > 0 and session.query(Intraday).count() > 0:
        return

    eod_dummpy_data = [
        ['2020-05-11', 'Bank 1', 'A1', 'SPAN', 3212.2],
        ['2020-05-11', 'Bank 1', 'A1', 'IMSM', 837.1], 
        ['2020-05-11', 'Bank 1', 'A2', 'SPAN', 8963.3],
        ['2020-05-11', 'Bank 1', 'A2', 'IMSM', 76687.9], 
        ['2020-05-11', 'Bank 2', 'A1', 'SPAN', 821.4], 
        ['2020-05-11', 'Bank 2', 'A1', 'IMSM', 8766.4],
    ]

    intraday_dummy_data = [
        ['2020-05-11', '18:00:00', 'Bank 1', 'A1', 'SPAN', 2882.2],
        ['2020-05-11', '18:00:00', 'Bank 1', 'A1', 'IMSM', 988.1], 
        ['2020-05-11', '18:00:00', 'Bank 1', 'A2', 'SPAN', 788.3],
        ['2020-05-11', '18:00:00', 'Bank 1', 'A2', 'IMSM', 908.9], 
        ['2020-05-11', '18:00:00', 'Bank 2', 'A1', 'SPAN', 123.4], 
        ['2020-05-11', '18:00:00', 'Bank 2', 'A1', 'IMSM', 8326.4], 
        # "last" intraday report of 2020-05-11 in CI050 table
        ['2020-05-11', '19:00:00', 'Bank 1', 'A1', 'SPAN', 3212.2],
        ['2020-05-11', '19:00:00', 'Bank 1', 'A1', 'IMSM', 837.1], 
        ['2020-05-11', '19:00:00', 'Bank 1', 'A2', 'SPAN', 8963.3],
        ['2020-05-11', '19:00:00', 'Bank 1', 'A2', 'IMSM', 76687.9], 
        ['2020-05-11', '19:00:00', 'Bank 2', 'A1', 'SPAN', 821.4], 
        ['2020-05-11', '19:00:00', 'Bank 2', 'A1', 'IMSM', 8766.4], 
        # "first" intraday report of 2020-05-12 in CI050 table
        ['2020-05-12', '08:00:00', 'Bank 1', 'A1', 'SPAN', 3212.2],
        ['2020-05-12', '08:00:00', 'Bank 1', 'A1', 'IMSM', 837.1], 
        ['2020-05-12', '08:00:00', 'Bank 1', 'A2', 'SPAN', 8963.3],
        ['2020-05-12', '08:00:00', 'Bank 1', 'A2', 'IMSM', 76687.9], 
        ['2020-05-12', '08:00:00', 'Bank 2', 'A1', 'SPAN', 821.4], 
        ['2020-05-12', '08:00:00', 'Bank 2', 'A1', 'SPAN', 8766.4], 
        # "second" intraday report of 2020-05-12 in CI050 table
        ['2020-05-12', '09:00:00', 'Bank 1', 'A1', 'SPAN', 3133.9],
        ['2020-05-12', '09:00:00', 'Bank 1', 'A1', 'IMSM', 137.1], 
        ['2020-05-12', '09:00:00', 'Bank 1', 'A2', 'SPAN', 2963.3],
        ['2020-05-12', '09:00:00', 'Bank 1', 'A2', 'IMSM', 74687.9], 
        ['2020-05-12', '09:00:00', 'Bank 2', 'A1', 'SPAN', 811.4], 
        ['2020-05-12', '09:00:00', 'Bank 2', 'A1', 'IMSM', 8366.4]
    ]
    
    # if there is no data in the tables, insert the dummy data
    insert_dummy_data(session, eod_dummpy_data, intraday_dummy_data)


def insert_dummy_data(session, eod_dummpy_data, intraday_dummy_data):
    """Insert dummy data into the tables"""
    session = get_session()
    for row in eod_dummpy_data:
        end_of_day = EndOfDay()
        end_of_day.date = row[0]
        end_of_day.clearing_number = row[1]
        end_of_day.account = row[2]
        end_of_day.margin_type = row[3]
        end_of_day.margin = row[4]
        session.add(end_of_day)
       

    for row in intraday_dummy_data:
        intraday = Intraday()
        intraday.date = row[0]
        intraday.time = row[1]
        intraday.clearing_number = row[2]
        intraday.account = row[3]
        intraday.margin_type = row[4]
        intraday.margin = row[5]
        session.add(intraday)
    
    session.commit()
