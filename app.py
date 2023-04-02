import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import EndOfDay, Intraday, get_session, create_tables
from plausibility_check import PlausibilityCheck


def send_email(data, title:str=''):
    print(f'title: {title}  -- data: {data}')

def logger(message, level):
    print(f"{level}: {message}")



def main():
    print('Start of main()')
    create_tables()
    session = get_session()

    # Get the end-of-day values of the previous day
    end_of_day = pd.read_sql(session.query(EndOfDay).filter().statement, session.bind)
    end_of_day = end_of_day.drop(columns=['id'])
    intraday = pd.read_sql(session.query(Intraday).filter().statement, session.bind)
    intraday = intraday.drop(columns=['id'])


    pc = PlausibilityCheck(end_of_day, intraday)
    if pc.check_previous_day():
        print('Alles OK. All the end-of-day values of the previous day are the same as the first intraday values.')
    else:
        print('ERROR in check_previous_day()')

    if pc.check_last_intraday():
        print('Alles Ok. the end-of-day values are the same as the last intraday values.')
    else:
        print('ERROR in check_last_intraday()')




if __name__ == '__main__':
    main()
