from enum import unique


class DataHandler:
    # Stations in dropdown
    _stations = []
    # Variables in dropdown for all selected stations
    _currentVariables = []
    # Currently selected stations
    _currentStations = []
    # Current table variables
    _currentTable = []

    # Dates from calendar selections
    _smearFromDate = "None"
    _smearToDate = "None"
    _statfiFromDate = "None"
    _statfiToDate = "None"

    # Query Handlers
    _smearHandler = "None"
    _statfiHandler = "None"

    # Smear Query parameters:
    _aggregation_type = 'NONE'
    _interval_length = 60
    _start_date = '2014-12-31T14:00:00.000'
    _end_date = '2015-01-01T17:00:00.000'
    _table_variable_name = 'VAR_EDDY.av_c'

    #Statfi query parameters:
    _STATFIitems = []
    _STATFIyears = ["2013", "2014", "2015"]

    # Statfi query response
    _STATFIx = "None"
    _STATFIy = "None"

    # Smear query response
    _SMEARx = "None"
    _SMEARy = "None"
    _SMEARunits = []
    _SMEARlabels = [""]

    # Smear statistics variables:
    _SMEARmin = "None"
    _SMEARmax = "None"
    _SMEARavg = "None"

    # Init
    def __init__(self, SmearHandler, StatfiHandler):
        self._smearHandler = SmearHandler
        self._statfiHandler = StatfiHandler
        self._stations = self.getStations()
        self._currentVariables = self.getCurrentVariables()
        self._currentTable = self.getCurrentVarTable()

    # Methods
    def getStations(self):
        return self._smearHandler.GetStations()[0]

    def getCurrentVariables(self):
        param, table = self._smearHandler.GetParams(self._currentStations)
        return param

    def getCurrentVarTable(self):
        param, table = self._smearHandler.GetParams(self._currentStations)
        return table

    def updateCurrentVariables(self):
        #self._currentVariables = ['CO2', 'SO2', 'NO']
        for station in self._currentStations:
            id = self._stations.index(station) + 1
            param, table = self._smearHandler.GetParams(id)
            # self._currentVariables = list(set(self._currentVariables).intersection(param))
            self._currentVariables = param

    def updateCurrentVarTables(self):
        for station in self._currentStations:
            id = self._stations.index(station) + 1
            param, table = self._smearHandler.GetParams(id)
            #self._currentTable = list(set(self._currentTable + table))
            self._currentTable = table

    # Makes a smear query using set interval and aggregation:
    def smearQuery(self):
        self._SMEARx, self._SMEARy, self._SMEARunits, self._SMEARlabels = self._smearHandler.FullQuery(self._start_date, self._end_date, [self._table_variable_name])
        #self._SMEARx, self._SMEARy = self._smearHandler.Query(self._aggregation_type, self._interval_length, self._start_date, self._end_date, self._table_variable_name)
        self._SMEARmin, self._SMEARmax, self._SMEARavg = self._smearHandler.AggregationQuery(self._start_date, self._end_date, [self._table_variable_name])
        pass

    # Makes a statfi query:
    def statfiQuery(self):
        if (len(self._STATFIitems) > 0 and len(self._STATFIyears) > 0):
            self._STATFIx, self._STATFIy = self._statfiHandler.Query(self._STATFIitems, self._STATFIyears)
        else:
            pass

    # Adds statfi data on smear plot from the applicable years:
    def mergeSMEAR_on_STATFI(self):

        # Make smear query:
        self.smearQuery()

        # Set years:
        years = []
        # Get units and labels from smear:
        units = self._SMEARunits[:]
        labels = self._SMEARlabels[:]

        # Get years from smear labels:
        for lab in self._SMEARx:
            # Make sure years are allowed by statfi:
            if int(lab[0:4]) > 1989 and int(lab[0:4]) < 2017:
                years.append(lab[0:4])

        # Get unique years:
        uniqueYears = []

        if len(list(set(years))) > 1:
            uniqueYears = list(set(years))
        elif len(list(set(years))) == 1:
            uniqueYears.append(years[0])

        # If allowed years exist:
        if len(uniqueYears) > 0:
            # Get statfi data:
            years_, result = self._statfiHandler.Query(self._STATFIitems, uniqueYears)

            yValues = []
            newY = self._SMEARy

            # New y values:
            for series in result:
                toAppend = []
                for j in years:
                    toAppend.append(float(series[years_.index(j)]))
                yValues.append(toAppend)

            # Append or extend:
            if newY == "None":
                newY = yValues
            else:
                if len(yValues) == 1:
                    newY.append(yValues[0])
                elif len(yValues) > 1:
                    newY.extend(yValues)

            # New units:
            if units == "None":
                units = self._STATFIitems
            else:
                if len(units) == 1:
                    units.append(self._STATFIitems[0])
                elif len(units) > 1:
                    units.extend(self._STATFIitems)
            # New labels:
            if labels == "None":
                labels = self._STATFIitems
            else:
                if len(labels) == 1:
                    labels.append(self._STATFIitems[0])
                elif len(units) > 1:
                    labels.extend(self._STATFIitems)

            return self._SMEARx, newY, units, labels

        # If statfi failed, keep smear:
        else:
            
            return self._SMEARx, self._SMEARy, self._SMEARunits, self._SMEARlabels


    # Get smear data on top of statfi from the first date of year:
    def mergeSTATFI_on_SMEAR(self):

        # Make statfi query:
        self.statfiQuery()

        # Get statfi values:
        years = self._STATFIx[:]
        units = self._STATFIitems[:]
        labels = self._STATFIitems[:]

        result = [[]]

        # Get a value from the first date of years: 
        for lab in years:
            # smear query times:
            startSmear = '{}-01-01T12:00:00.000'.format(lab)
            endSmear = '{}-01-01T13:00:00.000'.format(lab)

            # Get query:
            years_, res, unit, lab = self._smearHandler.FullQuery(startSmear, endSmear, [self._table_variable_name])

            # Extract result:
            if len(res[0]) > 0:
                result[0].append(res[0][0])

        # If smear data is available:
        if len(result)>0:
            # Append or extend y:
            newY = self._STATFIy

            if newY == "None":
                newY = result
            else:
                if len(result) == 1:
                    newY.append(result[0])
                elif len(result) > 1:
                    newY.extend(result)

            # Append or extend units:
            if units == "None":
                units = self._SMEARunits
            else:
                if len(units) == 1:
                    units.append(unit[0])
                elif len(units) > 1:
                    units.extend(unit)

            # Append or extend labels:
            if labels == "None":
                labels = self._SMEARlabels
            else:
                if len(labels) == 1:
                    labels.append(lab[0])
                elif len(units) > 1:
                    labels.extend(lab)

            return self._STATFIx, newY, units, labels

        # if smear data is unavailable, use statfi values only:
        else:
            return self._STATFIx, self._STATFIy, self._STATFIitems, self._STATFIitems


    def getSmearParameters(self):
        parameters = {
            "aggregation_type": self._aggregation_type, 
            "interval_length": self._interval_length, 
            "start_date": self._start_date, 
            "end_date": self._end_date, 
            "table_variable_name": self._table_variable_name
        }
        return parameters

    def getStatfiParameters(self):
        parameters = {
            "items": self._STATFIitems,
            "years": self._STATFIyears
        }
        return parameters