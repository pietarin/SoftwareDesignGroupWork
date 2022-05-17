from pydoc import describe
import unicodedata
from matplotlib.pyplot import table
from numpy import var
import requests
import json
from abc import ABC, abstractmethod

class QueryHandler(ABC):
    @abstractmethod
    def Query(self):
        #return  x, y, unit, description
        # x = [float/date]
        # y = [[float]]
        # unit = [str]
        # descriptiom = [str]
        pass


class SmearHandler(QueryHandler):      
    #Gets all stations
    #Return station names and ids in a separate lists
    def GetStations(self):
        #Fetch all SMEAR stations
        smear_stations = requests.get('https://smear-backend.rahtiapp.fi/search/station')
        
        #print(smear_stations.status_code)

        #Check if endpoint is valid
        if smear_stations.status_code != 200:
            raise ValueError("Wrong status code while fething stations")

        #parse_json contains all the stations' dcmiPoints, id's and names.
        data = smear_stations.text
        parse_json = json.loads(data)
        #print(parse_json)

        #Separate all the station names to a list
        names = []
        ids = []
        for i in range(len(parse_json)):
            names.append(parse_json[i]['name'])
            ids.append(parse_json[i]['id'])
        
        #print(names)
        #print(ids)

        return names, ids

    #Get all the accessible variables for the given station
    #Done manually for now
    def GetParams(self, stationId):
        #Params are found from 
        # id 1, 20;11 av_c ; SO2_1 NO_1
        # id 2, 4 CO2icos168 SO2168 NO168
        # id 3, 8;2 av_c_ep ; SO_2 NO
        # id 5, 10 av_c
        # id 6, 9 av_c
        # id 7, 16 av_c
        # id 8, 18 av_c
        # id 9, 26 av_c_LI72
        # id 12, 52 av_c
        # id 13, 54 av_c
        
        params = []
        if(stationId == 1):
            params.append("CO2")
            params.append("SO2")
            params.append("NO")
        elif(stationId == 2):
            params.append("CO2")
            params.append("SO2")
            params.append("NO")
        elif(stationId == 3):
            params.append("CO2")
            params.append("SO2")
            params.append("NO")
        elif(stationId == 5):
            params.append("CO2")
        elif(stationId == 6):
            params.append("CO2")
        elif(stationId == 7):
            params.append("CO2")
        elif(stationId == 8):
            params.append("CO2")
        elif(stationId == 9):
            params.append("CO2")
        elif(stationId == 12):
            params.append("CO2")
        elif(stationId == 13):
            params.append("CO2")
        else:
            pass
        
        return params
       
    #Gets station id (int) and table id (int) from stationParam (string) and variableParam (string)
    #Params: string, string
    #Returns -1 for values not found
    def GetStationAndTableId(self, stationParam, variableParam):
        
        stationId = -1
        tableId = -1

        if stationParam == 'VAR_EDDY':
            stationId = 1
            if variableParam == 'av_c':
                tableId = 20
        elif stationParam == 'VAR_META':
            stationId = 1
            if variableParam == 'SO2_1' or variableParam == 'NO_1':
               tableId = 11
        elif stationParam == 'HYY_META':
            stationId = 2
            if variableParam == 'CO2icos168' or variableParam == 'SO2168' or variableParam == 'NO168':
               tableId = 4
        elif stationParam == 'KUM_EDDY':
            stationId = 3
            if variableParam == 'av_c_ep':
               tableId = 8
        elif stationParam == 'KUM_META':
            stationId = 3
            if variableParam == 'SO_2' or variableParam == 'NO':
               tableId = 2
        elif stationParam == 'ERO_EDDY':
            stationId = 5
            if variableParam == 'av_c':
                tableId = 10
        elif stationParam == 'TOR_EDDY':
            stationId = 6
            if variableParam == 'av_c':
                tableId = 9
        elif stationParam == 'SII1_EDDY':
            stationId = 7
            if variableParam == 'av_c':
                tableId = 16
        elif stationParam == 'SII2_EDDY':
            stationId = 8
            if variableParam == 'av_c':
                tableId = 18
        elif stationParam == 'KVJ_EDDY':
            stationId = 9
            if variableParam == 'av_c_LI72':
                tableId = 26
        elif stationParam == 'VII_EDDY':
            stationId = 12
            if variableParam == 'av_c':
                tableId = 52
        elif stationParam == 'HAL_EDDY':
            stationId = 13
            if variableParam == 'av_c':
                tableId = 54
        
        return stationId, tableId
        
    #Gets variable id for the unitDescription search
    #NOT USED
    def GetVariableId(self, stationId, variableName):
        #Get all variables from station
        variables = requests.get('https://smear-backend.rahtiapp.fi/station/{}/table'.format(stationId))
        
        data = variables.text
        parse_json = json.loads(data)

        variableId = -1

        for i in range(len(parse_json)):
            if(parse_json[i]['name'] == variableName):
                variableId = parse_json[i]['id']
           
        #print(variableId)

        if variableId < 0:
            raise ValueError("Variable id not found")
        
        return variableId

    #Gets the unit and description of the given gas
    #Returns list of units and a list of descriptions;
    #Params: int, int, string
    def GetUnitDescription(self, stationId, variableId, gas):
        #query
        
        data_raw = requests.get('https://smear-backend.rahtiapp.fi/station/{}/table/{}/variable'.format(stationId, variableId))

        data = data_raw.text

        parse_json = json.loads(data)

        descriptions = []
        units = []

        for i in range(len(parse_json)):
            if(parse_json[i]['name'] == gas):
                descriptions.append(parse_json[i]['description'])
                units.append(parse_json[i]['unit'])
            

        #print(descriptions)  :: Throws error if printed

        #str1 = descriptions[0]
        #print(str1.encode('ascii', 'ignore'))

        #print(units) #:: Print this to see units

        #changes the format/encoding of descriptions from "SO₂ concentration 9 m" to "SO2 concentration 9 m"
        desc = [unicodedata.normalize('NFKD', x) for x in descriptions]
        #print(desc) #:: Print this to see descriptions

        return units, desc

    #Does the Query for the Min Max and Average values of the selected data
    #Returns MIN, MAX, AVG values from the given time period
    #Return only most min,max,avg values compared to each station/variable (Return only one Min, Max, AVG value)
    def AggregationQuery(self, start_date, end_date, table_variable_name_list):

        min_address = 'https://smear-backend.rahtiapp.fi/search/timeseries?aggregation=MIN&interval=60&from={}&to={}'.format(start_date, end_date)
        max_address = 'https://smear-backend.rahtiapp.fi/search/timeseries?aggregation=MAX&interval=60&from={}&to={}'.format(start_date, end_date)
        avg_address = 'https://smear-backend.rahtiapp.fi/search/timeseries?aggregation=ARITHMETIC&interval=60&from={}&to={}'.format(start_date, end_date)
        
        parts = ""

        #Put together a full request of multiple stations
        for variable in table_variable_name_list:
            parts += '&tablevariable={}'.format(variable)

        smear_min_series = requests.get(f"{min_address}{parts}")
        smear_max_series = requests.get(f"{max_address}{parts}")
        smear_avg_series = requests.get(f"{avg_address}{parts}")

        #parse_json{min,max,avg} contains all the stations' variable tables
        data_min = smear_min_series.text
        data_max = smear_max_series.text
        data_avg = smear_avg_series.text

        parse_json_min = json.loads(data_min)
        parse_json_max = json.loads(data_max)
        parse_json_avg = json.loads(data_avg)
        
        # Convert everything to dictionary:
        TimeSeriesMIN = parse_json_min['data']
        TimeSeriesMAX = parse_json_max['data']
        TimeSeriesAVG = parse_json_avg['data']

        print(TimeSeriesMIN)
        print(TimeSeriesMAX)
        print(TimeSeriesAVG)

        temporary = []
        #variables = []

        for variable in table_variable_name_list:
            for sample in TimeSeriesMIN:
                temporary.append(sample[variable])
                #variables.append(variable)

        print(temporary)
        #print(variables)

        Min = min(temporary)
        temporary.clear()


        for variable in table_variable_name_list:
            for sample in TimeSeriesMAX:
                temporary.append(sample[variable])
                #variables.append(variable)

        print(temporary)
        #print(variables)

        Max = max(temporary)
        temporary.clear()


        for variable in table_variable_name_list:
            for sample in TimeSeriesAVG:
                temporary.append(sample[variable])
                #variables.append(variable)

        print(temporary)
        #print(variables)

        Avg = sum(temporary) / len(temporary)
        temporary.clear()


        print(Min)
        print(Max)
        print(Avg)

        return Min, Max, Avg


    #Coes the JSON Query for multiple stations and table_variables
    #Also gets the units and descriptions of all table_variables
    #Params: table_variable_name_list = [table_variable_name, table_variable_name]
    #Returns: y(list[list[float]]), x(list[string]), units(list[list[string]]), descriptions(list[list[string]])
    def FullQuery(self, start_date, end_date, table_variable_name_list):
        

        address = 'https://smear-backend.rahtiapp.fi/search/timeseries?aggregation=NONE&interval=60&from={}&to={}'.format(start_date, end_date)
        parts = ""


        stations = []
        variables = []

        #Put together a full request of multiple stations
        for variable in table_variable_name_list:
            parts += '&tablevariable={}'.format(variable)
            
            #Splits the table_variable to station and variable
            #For unit and description fetching
            string = variable.split('.')
            stations.append(string[0])
            variables.append(string[1])

        #Make query of the requested variables
        smear_time_series = requests.get(f"{address}{parts}")

        #parse_json contains all the stations' variable tables
        data = smear_time_series.text
        parse_json = json.loads(data)
        
        # Convert to dictionary:
        TimeSeriesSMEAR = parse_json['data']


        x = []
        y = [[] for i in range(len(table_variable_name_list))]
     
        #Extract X and Y to lists:
        for sample in TimeSeriesSMEAR:
            index = 0
            x.append(sample['samptime'])

            for variable in table_variable_name_list:
                y[index].append(sample[variable])

                index += 1

        print(x)
        print(y)


        #Get units and descriptions for all table_variables
        units = []
        descriptions = []

        for item in range(0, len(table_variable_name_list)):
            #gets the needed parameters
            stationId, tableId = self.GetStationAndTableId(stations[item], variables[item])

            #Gets units and descriptions with needed parameters
            unit, desc = self.GetUnitDescription(stationId, tableId, variables[item])

            units.append(unit)
            descriptions.append(desc)

        print(units)
        print(descriptions)

        return x, y, units, descriptions

    #Does the JSON Query
    #Returns x and y values
    #Needs to add unit adn decription to the return...
    def Query(self, aggregation_type, interval_length, start_date, end_date, table_variable_name):
        # Make a query of the requested variables:
        smear_time_series = requests.get('https://smear-backend.rahtiapp.fi/search/timeseries?aggregation={}&interval={}&from={}&to={}&tablevariable={}'.format(aggregation_type, interval_length, start_date, end_date, table_variable_name))
        #parse_json contains all the stations' variable tables
        data = smear_time_series.text
        parse_json = json.loads(data)
        
        # Convert to dictionary:
        TimeSeriesSMEAR = parse_json['data']

        # X (time) and Y (value) lists:
        x = []
        y = [[]]

        # Extract X and Y to lists:
        for sample in TimeSeriesSMEAR:
            x.append(sample['samptime'])
            y[0].append(sample[table_variable_name])


        #Get the othe return values

        #Separate table and variable
        #parts = table_variable_name.split(".")
        #variable = parts[2]

        return x, y


class StatfiHandler(QueryHandler):
    #Palautus
    #(STATFI, aika akseli(x), list of list (y), LIST muuttujien yksiköt, LIST muuttujien nimet) 
    def Query(self, items, years):
        url1 = 'https://pxnet2.stat.fi:443/PXWeb/api/v1/en/ymp/taulukot/Kokodata.px'
        # An empty query where the parameters (variables and years) are fed:
        raw_query = '{"query": [{"code": "Tiedot","selection": {"filter": "item","values": []}},{"code": "Vuosi","selection": {"filter": "item","values": []}}]}'

        # Convert query to dictionary:
        query = json.loads(raw_query)
        # Insert query items and years into the query dict:
        query['query'][0]['selection']['values'] = items
        query['query'][1]['selection']['values'] = years

         # Convert query to JSON:
        data = json.dumps(query)

         # Post query:
        post_req = requests.post(url1, data=data)

        # Get values and labels (year):
        values = json.loads(post_req.text)["value"]
        labels = list(json.loads(post_req.text)["dimension"]["Vuosi"]["category"]["label"].values())

        #Just a little cheeky way to turn "Khk_yht" values to proper form
        for i, value in enumerate(values):
            #print(value)
            if value > 1000:
                values[i] = value / 1000

        #print(values)
        #print(labels)

        # The values are extractred in the prder of variables into list of lists res:
        res = [[] for i in range(len(items))]
        for i in range(len(items)):
            start = i * len(labels)
            end = (i+1)*len(labels)
            for value in range(start, end):
                res[i].append(values[value])


        return labels, res



def main():
    com = SmearHandler()
    com.GetStations()
   
   # SMEAR query parameters:
    aggregation_type = 'MAX'
    interval_length = 60
    start_date = '2022-01-19T14:00:00.000'
    end_date = '2022-01-19T17:00:00.000'
    #table_variable_name = 'VAR_EDDY.av_c'
    table_variable_name = ['VAR_META.SO2_1', 'KUM_META.SO_2', 'HYY_META.SO2168']

    #SMEARx, SMEARy = com.Query(aggregation_type, interval_length, start_date, end_date, table_variable_name)

    #print(SMEARx)
    #print(SMEARy)
    
    #com.GetVariableId(1, 'VAR_META')
    #com.GetUnitDescription(1, 11, "SO2_1")

    # STATFI query parameters:
    items = ["Khk_yht", "Khk_yht_index", "Khk_yht_las", "Khk_yht_las_index"]
    #items = ["Khk_yht_index"]
    years = ["2010", "2011", "2012", "2014", "2015", "2016"]

    cim = StatfiHandler()
    x, y = cim.Query(items, years)

    print(x)
    print(y)


    #com.AggregationQuery(start_date, end_date, table_variable_name)

    #Min, Max, Avg = com.AggregationQuery(start_date, end_date, table_variable_name)

    
    #print(Min)
    #print(Max)
    #print(Avg)
    
    #com.FullQuery(start_date, end_date, table_variable_name)




main()

