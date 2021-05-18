#!/usr/bin/python

import json,re

input_dir = "../output"
input_file = "bilbzzz429.dom101.mapres.sjson"

jf = "%s/%s" % ( input_dir, input_file )
json_file = open( jf, 'r' )
host_json = json.loads( json_file.read() )

# Get host_collections
print host_json['host_collections'][0]['name']

# Get source capsule name
print host_json['content_facet_attributes']['content_source']['name']

# Get OS version
print host_json['facts']['distribution::version']

# Get all IPv4 address
for key in host_json['facts'].keys ():

  # On cherche la pattern qui nous interesse pour cibler les ip
  result = re.search( "net::interface.*::ipv4_address$" , key)
  if result :

    print host_json['facts'][ key ]

# Get activation keys
index = 0
for item in host_json['subscription_facet_attributes']['activation_keys']:
 
  print host_json['subscription_facet_attributes']\
                 ['activation_keys'][index]['name']
  index = index + 1

