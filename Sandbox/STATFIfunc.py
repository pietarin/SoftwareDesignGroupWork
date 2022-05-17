import requests
import json

def STATFItest(items, years):

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

    # The values are extractred in the prder of variables into list of lists res:
    res = []
    for i in range(len(labels)):
        res.append(values[(2*i):(2*(i+1))])

    return labels, res
