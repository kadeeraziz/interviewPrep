import pandas as pd
import datetime as dt
import pytest
from plausibility_check import PlausibilityCheck

def test_plausibility_check():
    
    # Create test data
    end_of_day = pd.DataFrame([
        ['2020-05-11', 'Bank 1', 'A1', 'SPAN', 3212.2],
        ['2020-05-11', 'Bank 1', 'A1', 'IMSM', 837.1], 
        ['2020-05-11', 'Bank 1', 'A2', 'SPAN', 8963.3],
        ['2020-05-11', 'Bank 1', 'A2', 'IMSM', 76687.9], 
        ['2020-05-11', 'Bank 2', 'A1', 'SPAN', 821.4], 
        ['2020-05-11', 'Bank 2', 'A1', 'SPAN', 8766.4],
    ])
    
   
    intraday = pd.DataFrame([
        ['2020-05-11', '18:00:00', 'Bank 1', 'A1', 'SPAN', 2882.2],
        ['2020-05-11', '18:00:00', 'Bank 1', 'A1', 'IMSM', 988.1], 
        ['2020-05-11', '18:00:00', 'Bank 1', 'A2', 'SPAN', 788.3],
        ['2020-05-11', '18:00:00', 'Bank 1', 'A2', 'IMSM', 908.9], 
        ['2020-05-11', '18:00:00', 'Bank 2', 'A1', 'SPAN', 123.4], 
        ['2020-05-11', '18:00:00', 'Bank 2', 'A1', 'IMSM', 8326.4], 
        ['2020-05-11', '19:00:00', 'Bank 1', 'A1', 'SPAN', 3212.2],
        ['2020-05-11', '19:00:00', 'Bank 1', 'A1', 'IMSM', 837.1], 
        ['2020-05-11', '19:00:00', 'Bank 1', 'A2', 'SPAN', 8963.3],
        ['2020-05-11', '19:00:00', 'Bank 1', 'A2', 'IMSM', 76687.9], 
        ['2020-05-11', '19:00:00', 'Bank 2', 'A1', 'SPAN', 821.4], 
        ['2020-05-11', '19:00:00', 'Bank 2', 'A1', 'SPAN', 8766.4], 
        ['2020-05-12', '08:00:00', 'Bank 1', 'A1', 'SPAN', 3212.2],
        ['2020-05-12', '08:00:00', 'Bank 1', 'A1', 'IMSM', 837.1], 
        ['2020-05-12', '08:00:00', 'Bank 1', 'A2', 'SPAN', 8963.3],
        ['2020-05-12', '08:00:00', 'Bank 1', 'A2', 'IMSM', 76687.9], 
        ['2020-05-12', '08:00:00', 'Bank 2', 'A1', 'SPAN', 821.4], 
        ['2020-05-12', '08:00:00', 'Bank 2', 'A1', 'SPAN', 8766.4], 
        ['2020-05-12', '09:00:00', 'Bank 1', 'A1', 'SPAN', 3133.9],
        ['2020-05-12', '09:00:00', 'Bank 1', 'A1', 'IMSM', 137.1], 
        ['2020-05-12', '09:00:00', 'Bank 1', 'A2', 'SPAN', 2963.3],
        ['2020-05-12', '09:00:00', 'Bank 1', 'A2', 'IMSM', 74687.9], 
        ['2020-05-12', '09:00:00', 'Bank 2', 'A1', 'SPAN', 811.4], 
        ['2020-05-12', '09:00:00', 'Bank 2', 'A1', 'IMSM', 8366.4]
    ])

    end_of_day.columns = ['date', 'clearing_number', 'account', 'margin_type', 'margin']
    intraday.columns = ['date', 'time', 'clearing_number', 'account', 'margin_type', 'margin']
    
    # create plausibility check object
    pc = PlausibilityCheck(end_of_day, intraday)
    
    # test check_previous_day method
    assert pc.check_previous_day() == True


    # test check_last_intraday method
    assert pc.check_last_intraday() == True
    
   

    # test when there are unmatched intraday records
    end_of_day = pd.DataFrame([
        ['2023-03-30', 'Bank 1', 'A1', 'SPAN', 5214.1],
        ['2023-03-30', 'Bank 1', 'A1', 'IMSM', 1234.5], 
        ['2023-03-30', 'Bank 2', 'B1', 'SPAN', 3482.9], 
        ['2023-03-30', 'Bank 2', 'B1', 'IMSM', 1521.1],
        ['2022-03-29', 'Bank 1', 'A1', 'SPAN', 5167.3],
        ['2022-03-29', 'Bank 1', 'A1', 'IMSM', 1143.2], 
        ['2022-03-29', 'Bank 2', 'B1', 'SPAN', 3421.4], 
        ['2022-03-29', 'Bank 2', 'B1', 'IMSM', 1456.8],
    ])
    
   
    intraday = pd.DataFrame([
        ['2023-03-29', '08:00:00', 'Bank 1', 'A3', 'SPAN', 4311.2],
        ['2023-03-29', '08:00:00', 'Bank 1', 'A3', 'IMSM', 137.2], 
        ['2023-03-29', '08:00:00', 'Bank 1', 'A4', 'SPAN', 8963.3],
        ['2023-03-29', '08:00:00', 'Bank 1', 'A4', 'IMSM', 73687.9], 
        ['2023-03-29', '08:00:00', 'Bank 2', 'A2', 'SPAN', 921.4], 
        ['2023-03-29', '08:00:00', 'Bank 2', 'A2', 'IMSM', 7766.4]
    ])

    end_of_day.columns = ['date', 'clearing_number', 'account', 'margin_type', 'margin']
    intraday.columns = ['date', 'time', 'clearing_number', 'account', 'margin_type', 'margin']
    
    # create plausibility check object
    pc_unmatched = PlausibilityCheck(end_of_day, intraday)

    # test check_previous_day method
    assert pc_unmatched.check_previous_day() == False


    # test check_last_intraday method
    assert pc_unmatched.check_last_intraday() == False


    # test when end-of-day and intraday DataFrames are empty
    empty_df = pd.DataFrame()
    with pytest.raises(ValueError):
        pc_empty = PlausibilityCheck(empty_df, empty_df)
        pc_empty.check_previous_day()
    with pytest.raises(ValueError):
        pc_empty = PlausibilityCheck(empty_df, empty_df)
        pc_empty.check_last_intraday()
    