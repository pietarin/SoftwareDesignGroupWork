import requests
import json

#Fetch all smear stations. 
#You can look at the data at: https://smear-backend.rahtiapp.fi/search/station
smear_stations = requests.get('https://smear-backend.rahtiapp.fi/search/station')
#Check if the API endpoint is valid (entirely optional, this step can be removed)
print(smear_stations.status_code)
#parse_json contains all the stations' dcmiPoints, id's and names.
data = smear_stations.text
parse_json = json.loads(data)
print(parse_json)
#An example station is stored into a variable and printed out
station_example = parse_json[0]
print("\nexample station:", station_example, "\n")


stationId = 0
#Fetch a specific stations' variable tables, station 0 in this case. 
#You can look at the data at: https://smear-backend.rahtiapp.fi/search/station/0
smear_station = requests.get('https://smear-backend.rahtiapp.fi/station/{}/table'.format(stationId))
#Check if the API endpoint is valid (entirely optional, this step can be removed)
print(smear_station.status_code)
#parse_json contains all the stations' variable tables
data = smear_station.text
parse_json = json.loads(data)
print(parse_json)
#An example variable table is stored into a variable and printed out
variable_table_example = parse_json[0]
print("\nexample variable table:", variable_table_example)


tableId = 11
#Fetch a specific stations' tables' variables, station 0 table 11 in this case. 
#You can look at the data at: https://smear-backend.rahtiapp.fi/search/station/0/table/11/variable
variables_in_table = requests.get('https://smear-backend.rahtiapp.fi/station/{}/table/{}/variable'.format(stationId, tableId))
#Check if the API endpoint is valid (entirely optional, this step can be removed)
print(variables_in_table.status_code)
#parse_json contains all the stations' variable tables
data = variables_in_table.text
parse_json = json.loads(data)

#Only uncomment the below if you want to see ALL the variables.
#print(parse_json)

#An example variable table is stored into a variable and printed out. There are A LOT of these

variables_in_table_example = parse_json
#Only uncomment the below if you want to see ALL the variables.
#print("\nvariables in table example:", variables_in_table_example)


#An example using only some relevant variables
#Using query format: 
#https://smear-backend.rahtiapp.fi/search/timeseries?aggregation=<AGGREGATION_TYPE>&interval=<INTERVAL_LENGTH>&from=<START_DATE>&to=<END_DATE>&tablevariable=<TABLE_VARIABLE_NAME>
#Read more: https://course-gitlab.tuni.fi/comp.se.110-software-design_spring_2022/examples/-/blob/master/software-design-api-examples-2022.md#time-series-query-examples 
#You can look at the data at:
#https://smear-backend.rahtiapp.fi/search/timeseries?aggregation=MAX&interval=60&from=2022-01-19T14:00:00.000&to=2022-01-19T17:00:00.000&tablevariable=VAR_EDDY.av_c
aggregation_type = 'MAX'
interval_length = 60
start_date = '2022-01-19T14:00:00.000'
end_date = '2022-01-19T17:00:00.000'
table_variable_name = 'VAR_EDDY.av_c'
#Fetch the hourly maximums for CO2 at Värriö between 2pm and 5pm at 19th May 2022
smear_time_series = requests.get('https://smear-backend.rahtiapp.fi/search/timeseries?aggregation={}&interval={}&from={}&to={}&tablevariable={}'.format(aggregation_type, interval_length, start_date, end_date, table_variable_name))
#Check if the API endpoint is valid (entirely optional, this step can be removed)
print(smear_time_series.status_code)
#parse_json contains all the stations' variable tables
data = smear_time_series.text
parse_json = json.loads(data)
print(parse_json)
#An example variable table is stored into a variable and printed out
smear_time_series_example = parse_json
print("\nexample Time series:", smear_time_series_example)


# Testing SMEAR conversion:

testTimeSeriesSMEAR = parse_json['data']

testX = []
testY = []

for sample in testTimeSeriesSMEAR:
    testX.append(sample['samptime'])
    testY.append(sample['VAR_EDDY.av_c'])

print("\n")
print("Test time labels: {}\n".format(testX))
print("Test y values: {}\n".format(testY))
