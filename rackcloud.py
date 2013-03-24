#!/usr/bin/python

import argparse
import os
import pyrax
import sys

def create(args):
  if args.type=="server":
    if args.verbose:
      print 'Connecting to Cloud Servers Services'
    cs = pyrax.connect_to_cloudservers(pyrax.default_region)
    flavors = cs.flavors.list()
    images = cs.images.list()
    #Image Identification and Selection
    image = args.image;
    image_select = []
    for img in images:
      if args.image.lower() in img.name.lower():
        image_select.append([img.id,img.name])
    for id,name in image_select:
      print id + " - " + name
    if len(image_select) > 1:
      print "Enter Image Id to use:"
      image = sys.stdin.readline()
    else:
      image = image_select[0][0]
    if args.verbose:
      print "Using Image Id:" + image
  exit()

def read(args):
  print args.id
  exit()

parser = argparse.ArgumentParser(description='Do something neat in the Rackspace Cloud',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-u','--user',help='Rackspace API user')
parser.add_argument('-k','--apikey',help='Rackspace user API key')
creds_path = os.environ['HOME'] + "/.rackspace_cloud_credentials"
parser.add_argument('--creds',default=creds_path,help="Alternate Rackspace Cloud Credentials File to use.")
parser.add_argument('-r','--region',help='Cloud region to operate on.',default="DFW",choices=['DFW','ORD','LON'])
parser.add_argument('-t','--type',help='Type of Rackspace Cloud Device to operate on.',default='server',choices=['server','db','lb','files','blockstorage','dns','networks'])
parser.add_argument('-v','--verbose',action='store_true',help='Enable verbose output of actions.')
subparsers = parser.add_subparsers(help='sub command help')

parser_c = subparsers.add_parser('create', help='Create command options',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser_c.add_argument('-n','--number',type=int, help='Number of instances to create.',default=1)
parser_c.add_argument('-f','--flavor',help='Instance Flavor (regex) to be used for create functions',default='512MB Standard Instance')
parser_c.add_argument('-i','--image',help='Image (regex) to be used for create functions',default='Centos 6')
parser_c.add_argument('--prefix',help='Prefix to use for hostnames',default='server')
parser_c.set_defaults(func=create)

parser_r = subparsers.add_parser('read', help='View Rackspace Cloud Detail options',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser_r.add_argument('-i','--id',help='unique id of device to operate on')
parser_r.set_defaults(func=read)

args = parser.parse_args()

try:
  if args.user and args.apikey:
    if args.verbose:
      print "Using user (" + args.user + ") and apikey from command line."
    pyrax.set_credentials(args.user,args.apikey)
  else:
    if args.verbose:
      print "Using Credentials in: " + args.creds
    pyrax.set_credential_file(args.creds)
except pyrax.exceptions.FileNotFound:
  print "Could not find credentials file: " + args.creds
  exit()
except pyrax.exceptions.AuthenticationFailed:
  print "Unable to authenicate to cloud identity services. Check credentials."
  exit()
except:
  print "Unknown error authenticating to cloud identity services."
  traceback.print_exc()
  exit()

pyrax.default_region = args.region
if args.verbose:
  print "Authenticated to Rackspace Cloud Identity:" + str(pyrax.identity.authenticated)

args.func(args)

