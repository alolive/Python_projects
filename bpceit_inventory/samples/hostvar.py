#!/usr/bin/python

import json

print('serialization')
myHostObj = { "name":"John", "age":30, "car":None }
myHostvarObj = { "MyDriverTeam" : myHostObj } 

##convert object to json
serialized= json.dumps(myHostvarObj, sort_keys=True, indent=3)
print(serialized)
## now we are gonna convert json to object
deserialization=json.loads(serialized)
print(deserialization)

myHostObj['feetsize'] = ["8 UK","42 fr"]

serialized= json.dumps(myHostvarObj, sort_keys=True, indent=3)
print(serialized)


#data['people'] = []
#data['people'].append({
#    'name': 'Scott',
#    'website': 'stackabuse.com',
#    'from': 'Nebraska'
#})
#data['people'].append({
#    'name': 'Larry',
#    'website': 'google.com',
#    'from': 'Michigan'
#})
#data['people'].append({
#    'name': 'Tim',
#    'website': 'apple.com',
#    'from': 'Alabama'
#})
#
#
