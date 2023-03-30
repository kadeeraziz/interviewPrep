
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
    - The unmatched_previous_day_records are the end-of-day values of the previous day that do not have matching first intraday values.
    - The unmatched_last_intraday_records are the end-of-day values that do not have matching last intraday values.
    """

    def __init__(self, end_of_day: pd.DataFrame, intraday: pd.DataFrame) -> None:
        self.end_of_day = end_of_day
        self.intraday = intraday
        self.unmatched_previous_day_records = []
        self.unmatched_last_intraday_records = []
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


    def check_previous_day(self):
        """
        Check if the end-of-day values of the previous day are the same as the first intraday values.

        Returns:
            bool: True if all end_of_day values of the previous day have matching first intraday values, False otherwise.
        """
        
        has_match:bool = False
        for eod_row in self.end_of_day.itertuples(index=False):
            has_match = False
            for intra_row in self.intraday.itertuples(index=False):
                if eod_row.date + pd.DateOffset(days=1) == intra_row.date and intra_row.time == dt.time(8, 0, 0):
                    intra_row_no_date = intra_row._asdict()
                    eod_row_no_date = eod_row._asdict()
                    if 'time' in intra_row_no_date:
                        del intra_row_no_date['time']
                    if 'date' in intra_row_no_date:
                        del intra_row_no_date['date']
                    if 'date' in eod_row_no_date:
                        del eod_row_no_date['date']
                    
                    if eod_row_no_date == intra_row_no_date:
                        has_match = True
                        break
                    
            if not has_match:
                has_match = False
                self.unmatched_previous_day_records.append(eod_row)
                
        return has_match
    

    def check_last_intraday(self)->bool:
        """
        Check if the end-of-day values are the same as the last intraday values.

        Returns:
            bool: True if all end_of_day values have matching last intraday values, False otherwise.
        """
        
        has_match:bool = False
        for eod_row in self.end_of_day.itertuples(index=False):
            has_match = False
            for intra_row in self.intraday.itertuples(index=False):
                if eod_row.date == intra_row.date and intra_row.time == dt.time(19, 0, 0):
                    intra_row_no_time = intra_row._asdict()
                    if 'time' in intra_row_no_time:
                        del intra_row_no_time['time']
                        
                    if intra_row_no_time == eod_row._asdict():
                        has_match = True
                        break
            if not has_match:
                has_match = False
                self.unmatched_last_intraday_records.append(eod_row)

        return has_match
    