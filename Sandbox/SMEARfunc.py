import requests
import json

def SMEARtest(aggregation_type, interval_length, start_date, end_date, table_variable_name):

    # Make a query of the requested variables:
    smear_time_series = requests.get('https://smear-backend.rahtiapp.fi/search/timeseries?aggregation={}&interval={}&from={}&to={}&tablevariable={}'.format(aggregation_type, interval_length, start_date, end_date, table_variable_name))
    #parse_json contains all the stations' variable tables
    data = smear_time_series.text
    parse_json = json.loads(data)

    # Testing SMEAR conversion:
    # Convert to dictionary:
    testTimeSeriesSMEAR = parse_json['data']

    # X (time) and Y (value) lists:
    testX = []
    # Temporary structure to handle the structure where there are multiple y time series:
    testY = [[]]

    # Extract X and Y to lists:
    for sample in testTimeSeriesSMEAR:
        testX.append(sample['samptime'])
        testY[0].append(sample[table_variable_name])

    return testX, testY