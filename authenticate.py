#!/usr/bin/python

import pyrax
import json
import os
import traceback
import sys
import getopt
import re

#Set options
region = ''
flavor = ''
image = ''
user = ''
apikey = ''
try:
   opts, args = getopt.getopt(sys.argv[1:],"hr:f:i:u:k:",["region=","flavor=","image=","help","user=","apikey="])
except getopt.GetoptError:
   print sys.argv[0] + ' [-r,--region <region>] [-f,--flavor <flavor>] [-i,--image <image>] [-u,--user <apiusername> -k,--apikey <apikey>]'
   sys.exit(2)
for opt, arg in opts:
   if opt in ('-h',"--help"):
     print sys.argv[0] + ' [-r,--region <region>] [-f,--flavor <flavor>] [-i,--image <image>] [-u,--user <apiusername> -k,--apikey <apikey>]'
     sys.exit()
   elif opt in ("-r", "--region"):
     region = arg
   elif opt in ("-f", "--flavor"):
     flavor = arg
   elif opt in ("-i", "--image"):
     image = arg
   elif opt in ("-u", "--user"):
     user = arg
   elif opt in ("-k", "--apikey"):
     apikey = arg

#Authenticate using either user/apikey from options or default credential file
credfile = ''
try:
  if user and apikey:
    print "Using user (" + user + ") and apikey from command line."
    pyrax.set_credentials(user,apikey)
  else:
    credfile = os.environ['HOME'] + "/.rackspace_cloud_credentials"
    print "Using Credentials in: " + credfile
    pyrax.set_credential_file(credfile)
except pyrax.exceptions.FileNotFound:
  print "Could not find credentials file: " + credfile
  exit()
except pyrax.exceptions.AuthenticationFailed:
  print "Unable to authenicate to cloud identity services. Check credentials."
  exit()
except:
  print "Unknown error authenticating to cloud identity services."
  traceback.print_exc()
  exit()

#Set region if it has been given. Accept only valid regions or else use default.
if region in ('DFW','ORD','LON'):
  pyrax.default_region = region
else:
  print 'No Region or Invalid Region: ' + region 
  print 'Using Default.'
print "Authenticated to cloud identity."
print "Using region: " + pyrax.default_region

#Connect to cloud servers for specified region
cs = pyrax.connect_to_cloudservers(pyrax.default_region)
#print cs_dfw
#Get flavors and images
flavors = cs.flavors.list()
images = cs.images.list()
#for image in images:
#   print image.id," - ",image.name
#servers = cs.servers.list()
#for server in servers:
#   print server.id," - ",server.name
#   for type,ips in server.networks.items():
#     for ip in ips:
#       print type,":",ip

#Image Identification and Selection
if image is '':
  image = 'CentOS 6'
image_select = [] 
for img in images:
  if image.lower() in img.name.lower():
    image_select.append([img.id,img.name])
for id,name in image_select:
  print id + " - " + name
if len(image_select) > 1:
  print "Enter Image Id to use: "
  image = sys.stdin.readline()
else:
  image = image_select[0][0]
print "Using Image Id:" + image

#Flavor Identification and Selection
if flavor is '':
  flavor = '512MB Standard Instance'
flavor_select = []
for flav in flavors:
  reflav_match = re.findall(flavor, str(vars(flav)), flags=re.I)
  if reflav_match:
    flavor_select.append([flav.id,flav.name])
for id,name in flavor_select:
  print id + " - " + name
if len(flavor_select) > 1:
  print "Enter Flavor Id to use: "
  flavor = sys.stdin.readline()
elif len(flavor_select) is 0:
  print "Couldn't find any matching flavors. Exiting."
  exit()
else:
  flavor = flavor_select[0][0]
print "Using Flavor Id:" + flavor

#print json.dumps(servers)
#  pprint.pprint(flavor.id)
#  pprint.pprint(flavor.name)
#  #print flavor.id
#  #print flavor.name
#ord_512 = cs_ord.flavors.(0)
#print ord_flavors
