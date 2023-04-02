from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class EndOfDay(Base):
    __tablename__ = 'end_of_day'

    id = Column(Integer, primary_key=True)
    date = Column(String)
    cleaning_number = Column(Integer)
    account = Column(String)
    margin_type = Column(String)
    margin = Column(Integer)

    def __init__(self) -> None:
        super().__init__()

    def __repr__(self):
        return f"EndOfDay(date={self.date}, cleaning_number={self.cleaning_number}, account={self.account}, margin_type={self.margin_type}, margin={self.margin})"
    

class Intraday(Base):
    __tablename__ = 'intraday'

    id = Column(Integer, primary_key=True)
    date = Column(String)
    time = Column(String)
    cleaning_number = Column(Integer)
    account = Column(String)
    margin_type = Column(String)
    margin = Column(Integer)

    def __init__(self) -> None:
        super().__init__()

    def __repr__(self):
        return f"Intraday(date={self.date}, time={self.time}, cleaning_number={self.cleaning_number}, account={self.account}, margin_type={self.margin_type}, margin={self.margin})"



engine = create_engine('sqlite:///LZDB.db', echo=True)



# check if tables exist
if not inspect(engine).has_table('end_of_day') and not inspect(engine).has_table('intraday'):
    # create tables
    Base.create_all(blind=engine)




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


# create the dummy data

# Session = sessionmaker(bind=engine)
# session = Session()

#insert dummy data
# for row in eod_dummpy_data:
#     eod = EndOfDay()
#     eod.date = row[0]
#     eod.cleaning_number = row[1]
#     eod.account = row[2]
#     eod.margin_type = row[3]
#     eod.margin = row[4]
#     session.add(eod)

    
# for row in intraday_dummy_data:
#     intraday = Intraday()
#     intraday.date = row[0]
#     intraday.time = row[1]
#     intraday.cleaning_number = row[2]
#     intraday.account = row[3]
#     intraday.margin_type = row[4]
#     intraday.margin = row[5]
#     session.add(intraday)
    
# session.commit()







