
import pandas as pd
import datetime as dt


class PlausibilityCheck:
    """
    A class for performing plausibility check on end-of-day and intraday data.

    Information: 
    What is plausibility check?
    Plausibility checks are a set of validation checks
    that are performed on data to ensure that it is consistent, complete, and plausible.
    The goal of plausibility checks is to identify and flag data that is likely to be incorrect or erroneous.
    
    Attributes:
    end_of_day (pandas.DataFrame): A DataFrame of end-of-day values, 
    intraday (pandas.DataFrame): A DataFrame of intraday values, 
    """

    def __init__(self, end_of_day: pd.DataFrame, intraday: pd.DataFrame) -> None:
        self.end_of_day = end_of_day
        self.intraday = intraday
        self.unmatched_eod = []
    
    def check_previous_day(self):
        """
        Check if the end-of-day values of the previous day are the same as the first intraday values.

        Returns:
        bool: A boolean indicating if all EOD values of the previous day have matching first intraday values.
        """

        has_match = True
        unmatched = []
        for eod_row in self.end_of_day.itertuples(index=False):
            row_match = False
            for intra_row in self.intraday.itertuples(index=False):
                #check, if the eod values of the previous day are the same as the first intraday values
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
                unmatched.append(eod_row)
        return has_match, unmatched
    

    def check_eod_last_intraday(self):
        """
        Check if the end-of-day values are the same as the last intraday values.

        Returns:
        tuple: A tuple containing a boolean indicating if all eod values have matching last intraday values, and a list of rows in eod_df that don't have a match in intraday.
        """
        unmatched = []
        has_match = True
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
                unmatched.append(eod_row)
        return has_match, unmatched