import json
import urllib2
import urllib
import requests

input_data = { 'unit_id': '1',
               'c_value': 5000,
               'r_value': 2600,
               'g_value': 1400,
               'b_value': 1200
               }

print json.dumps(input_data)


url = 'https://coolscandeluxe.herokuapp.com/datadump'

#request = urllib2.Request(url)

#request.add_header('Content-Type', 'application/json')

#response = urllib2.urlopen(request, json.dumps(input_data)).read()

#print response

r = requests.post(url, data=json.dumps(input_data), 
                  headers={'Content-Type': 'application/json'})
response = r.text

print response
