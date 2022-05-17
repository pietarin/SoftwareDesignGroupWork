import requests
import json

url1 = 'https://pxnet2.stat.fi/PXWeb/api/v1/en/ymp/taulukot/Kokodata.px'

#Fetch all possible STATFI selections. 
statfi_selections = requests.get(url1)
#Check if the API endpoint is valid (entirely optional, this step can be removed)
print(statfi_selections.status_code)
#parse_json contains all the possible selections
data = statfi_selections.text
parse_json = json.loads(data)
#print(parse_json)
#possible selections are stored into a variable and printed out
selections_example = parse_json
print("\nall selections:", selections_example, "\n")

#The data tables are fetched from the API using a POST query where the selections are given as the content of the query.
url2 = 'https://pxnet2.stat.fi:443/PXWeb/api/v1/en/ymp/taulukot/Kokodata.px'
#Example 1:
#Fetch a table containing the yearly values for the "Intensity of greenhouse gas emissions" between 2002 and 2004.
data = '{"query": [{"code": "Tiedot","selection": {"filter": "item","values": ["Khk_yht_las"]}},{"code": "Vuosi","selection": {"filter": "item","values": ["2002", "2003", "2004"]}}]}'
post_req = requests.post(url2, data=data)

print(post_req.status_code)
print(post_req.text)

#Example 2:
#Fetch a table containing the yearly values for the 2 indexed greenhouse gas values for years 2010 and 2011.
data = '{"query": [{"code": "Tiedot","selection": {"filter": "item","values": ["Khk_yht_index", "Khk_yht_las_index"]}},{"code": "Vuosi","selection": {"filter": "item","values": ["2010", "2011"]}}]}'
post_req = requests.post(url2, data=data)

print(post_req.status_code)
print(post_req.text)


js = {"class":"dataset","label":"Environmental Accounting: Key Figures by Tiedot and Vuosi","source":"Statistics Finland","updated":"2012-06-26T06:00:00Z","id":["Tiedot","Vuosi"],"size":[2,2],"dimension":{"Tiedot":{"label":"Tiedot","category":{"index":{"Khk_yht_index":0,"Khk_yht_las_index":1},"label":{"Khk_yht_index":"Greenhouse gas emissions, indexed, year 1990 = 100","Khk_yht_las_index":"Intensity of greenhouse gases, indexed, year 1990 = 100"}}},"Vuosi":{"label":"Vuosi","category":{"index":{"2010":0,"2011":1},"label":{"2010":"2010","2011":"2011"}}}},"value":[107.4,96.4,72.43,63.38],"role":{"time":["Vuosi"]},"version":"2.0","extension":{"px":{"decimals":0}}}

js2 = {'Tiedot': {'label': 'Tiedot', 'category': {'index': {'Khk_yht_index': 0, 'Khk_yht_las_index': 1}, 'label': {'Khk_yht_index': 'Greenhouse gas emissions, indexed, year 1990 = 100', 'Khk_yht_las_index': 'Intensity of greenhouse gases, indexed, year 1990 = 100'}}}, 'Vuosi': {'label': 'Vuosi', 'category': {'index': {'2010': 0, '2011': 1}, 'label': {'2010': '2010', '2011': '2011'}}}}

js3 = {'label': 'Vuosi', 'category': {'index': {'2010': 0, '2011': 1}, 'label': {'2010': '2010', '2011': '2011'}}}

print(js["dimension"])
print(js2["Vuosi"])
print(js3["category"]["label"].values())

values = json.loads(post_req.text)["value"]
labels = list(json.loads(post_req.text)["dimension"]["Vuosi"]["category"]["label"].values())

print("\n")
print(values)
print("\n{}".format(labels))