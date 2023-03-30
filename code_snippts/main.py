#from .models import EndOfDay, Intraday
from plausibility_check import PlausibilityCheck
from .services import send_email, logger


def main():
    
    # fetch data from database
    # end_of_day = EndOfDay.objects.filter(date='2020-05-11')
    # intraday = Intraday.objects.filter(date__in=['2020-05-11', '2020-05-12'])

    # convert to pandas DataFrames
    # eod = pd.DataFrame(end_of_day.values())
    # intraday = pd.DataFrame(intraday.values())

    eod = pd.DataFrame([
        ['2020-05-11', 'Bank 1', 'A1', 'SPAN', 3212.2],
        ['2020-05-11', 'Bank 1', 'A1', 'IMSM', 837.1], 
        ['2020-05-11', 'Bank 1', 'A2', 'SPAN', 8963.3],
        ['2020-05-11', 'Bank 1', 'A2', 'IMSM', 76687.9], 
        ['2020-05-11', 'Bank 2', 'A1', 'SPAN', 821.4], 
        ['2020-05-11', 'Bank 2', 'A1', 'SPAN', 8766.4],
    ])

    eod.columns = ['date', 'clearing_number', 'account', 'margin_type', 'margin']

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
        ['2020-05-12', '08:00:00', 'Bank 2', 'A1', 'IMSM', 8766.4], 
        # "second" intraday report of 2020-05-12 in CI050 table
        ['2020-05-12', '09:00:00', 'Bank 1', 'A1', 'SPAN', 3133.9],
        ['2020-05-12', '09:00:00', 'Bank 1', 'A1', 'IMSM', 137.1], 
        ['2020-05-12', '09:00:00', 'Bank 1', 'A2', 'SPAN', 2963.3],
        ['2020-05-12', '09:00:00', 'Bank 1', 'A2', 'IMSM', 74687.9], 
        ['2020-05-12', '09:00:00', 'Bank 2', 'A1', 'SPAN', 811.4], 
        ['2020-05-12', '09:00:00', 'Bank 2', 'A1', 'IMSM', 8366.4]
    ])


    intraday.columns = ['date', 'time', 'clearing_number', 'account', 'margin_type', 'margin']

    p = PlausibilityCheck(eod, intraday)
    # print(p.check_previous_day())
    # print(p.unmatched_end_of_day_records)

    print(p.check_last_intraday())
    print(p.unmatched_end_of_day_records)

    if not p.check_last_intraday():
        if p.unmatched_end_of_day_records:
            data = {'date': p.unmatched_end_of_day_records}
            send_email(data)
            logger(p.unmatched_end_of_day_records, 'ERROR')

            
    


if __name__ == '__main__':
    main()