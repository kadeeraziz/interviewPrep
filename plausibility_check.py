
import pandas as pd
import datetime as dt


class PlausibilityCheck:
    """
    A class for performing plausibility check on end-of-day and intraday data.
    A plausibility check ensure the consistency of the data and flags any inconsistencies.
    
    Attributes:
        end_of_day (pandas.DataFrame): A DataFrame of end-of-day values, 
        intraday (pandas.DataFrame): A DataFrame of intraday values, 

    Methods:
        check_previous_day(): Check if the end-of-day values of the previous day are the same as the first intraday values.
        check_last_intraday(): Check if the end-of-day values are the same as the last intraday values.

    Note:
    - The first intraday values of the day are the values at 8:00:00.
    - The last intraday values of the day are the values at 19:00:00.
    """

    def __init__(self, end_of_day: pd.DataFrame, intraday: pd.DataFrame) -> None:
        self.end_of_day = end_of_day
        self.intraday = intraday
        self.preprocess()
    
    def preprocess(self)->None:
        """
        Preprocesses the end-of-day and intraday DataFrames by converting date and time columns
        to datetime objects. Raises a ValueError if either DataFrame is empty.
        """

        if self.end_of_day.empty or self.intraday.empty:
            raise ValueError("end-of-day and intraday DataFrames must not be empty.")
        
        self.end_of_day['date'] = pd.to_datetime(self.end_of_day['date'])
        self.intraday['date'] = pd.to_datetime(self.intraday['date'])
        self.intraday['time'] = self.intraday['time'].apply(lambda x: dt.datetime.strptime(x, '%H:%M:%S').time())


    def check_previous_day(self)->bool:
        """
        Check if the end-of-day values of the previous day are the same as the first intraday values.
        Send an email and logs if there are any unmatched records.

        Returns:
            bool: True if all end_of_day values have matching first intraday values, False otherwise.
        """
        
        # Get the first intraday values of the day
        processed_intraday = self.intraday.loc[(self.intraday['date']=='2020-05-12') & (self.intraday['time']==dt.time(8,0,0))]

        # Merge the end_of_day and intraday DataFrames
        merged_df = pd.merge(self.end_of_day, processed_intraday, on=['clearing_number', 'account', 'margin_type', 'margin'], how='outer')

        end_of_day_unmatched = merged_df[merged_df['date_y'].isnull()].drop(columns=['date_y', 'time'])

        intraday_unmatched = merged_df[merged_df['date_x'].isnull()].drop(columns=['date_x'])

        if  end_of_day_unmatched.empty and intraday_unmatched.empty:
            return True

        if not end_of_day_unmatched.empty:
            print('---------------------------------------------------------------')
            send_email(end_of_day_unmatched.to_dict('records'), 'end_of_day_unmatched')
            logger(end_of_day_unmatched.to_dict('records'), 'ERROR')
        if not intraday_unmatched.empty:
            print('---------------------------------------------------------------')
            send_email(intraday_unmatched.to_dict('records'), 'intraday_unmatched')
            logger(intraday_unmatched.to_dict('records'), 'ERROR')
    
        return False
    

    def check_last_intraday(self)->bool:
        """
        Check if the end-of-day values are the same as the last intraday values.
        Send an email and logs if there are any unmatched records.

        Returns:
            bool: True if all end_of_day values have matching last intraday values, False otherwise.
        """
        # Get the last intraday values of the day
        processed_intraday = self.intraday.loc[(self.intraday['date']=='2020-05-11') & (self.intraday['time'] == dt.time(19, 0, 0))]

        # Merge the end_of_day and intraday DataFrames
        merged_df = pd.merge(self.end_of_day, processed_intraday, on=['clearing_number', 'account', 'margin_type', 'margin'], how='outer')

        end_of_day_unmatched = merged_df[merged_df['date_y'].isnull()].drop(columns=['date_y', 'time'])

        intraday_unmatched = merged_df[merged_df['date_x'].isnull()].drop(columns=['date_x'])
     
        if  end_of_day_unmatched.empty and intraday_unmatched.empty:
            return True

        if not end_of_day_unmatched.empty:
            print('---------------------------------------------------------------')
            send_email(end_of_day_unmatched.to_dict('records'), 'end_of_day_unmatched')
            logger(end_of_day_unmatched.to_dict('records'), 'ERROR')
        if not intraday_unmatched.empty:
            print('---------------------------------------------------------------')
            send_email(intraday_unmatched.to_dict('records'), 'intraday_unmatched')
            logger(intraday_unmatched.to_dict('records'), 'ERROR')
    
        return False


def main():

    end_of_day = pd.DataFrame([
        ['2020-05-11', 'Bank 1', 'A1', 'SPAN', 3212.2],
        ['2020-05-11', 'Bank 1', 'A1', 'IMSM', 837.1], 
        ['2020-05-11', 'Bank 1', 'A2', 'SPAN', 8963.3],
        ['2020-05-11', 'Bank 1', 'A2', 'IMSM', 76687.9], 
        ['2020-05-11', 'Bank 2', 'A1', 'SPAN', 821.4], 
        ['2020-05-11', 'Bank 2', 'A1', 'SPAN', 8766.4],
    ])

    end_of_day.columns = ['date', 'clearing_number', 'account', 'margin_type', 'margin']

    intraday = pd.DataFrame([
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
    ])


    intraday.columns = ['date', 'time', 'clearing_number', 'account', 'margin_type', 'margin']

    pc = PlausibilityCheck(end_of_day, intraday)
    if pc.check_previous_day():
        print('Alles OK. All the end-of-day values of the previous day are the same as the first intraday values.')
    else:
        print('ERROR in check_previous_day()')

    if pc.check_last_intraday():
        print('Alles Ok. Check if the end-of-day values are the same as the last intraday values.')
    else:
        print('ERROR in check_last_intraday()')



def send_email(data, title:str=''):
    print(f'sending email...: title: {title}  -- records: {data}')

def logger(message, level):
    print(f"logging...: {level}: {message}")

if __name__ == '__main__':
    main()
    