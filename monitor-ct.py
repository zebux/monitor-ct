#!/usr/bin/python
# -*- coding: utf-8 -*-

'''

	@ author : Zebux <zebux@zebux.org>
	@copyright:  AGPLv3
             http://www.gnu.org/licenses/agpl.html

'''

import requests
import sys
import json
from datetime import datetime, timedelta

version = "v0.2"
nbr_days= 7

from optparse import OptionParser
usage = "usage: %prog [options] filenames / domain ..."
parser = OptionParser(usage)
#parser = OptionParser()
parser.add_option("-d", dest="domain", help="domain name to check")
parser.add_option("-v", "--version", action="store_true", dest="version", help="display the version")
parser.add_option("-f", dest="filenamearg", help="mass domain monitor option. File with one line per domain.")
parser.add_option("-t", type='int', dest="time", default=7, help="check certificate issue since <days number> days - default 7 days")

(options, args) = parser.parse_args()
'''
print 'domain     :', options.domain
print 'version    :', options.version
print 'file       :', options.filenamearg
print 'time       :', options.time
print 'Args :', args
'''

if options.version :
  print ""
  print "This script monitor certificat transparency from a domain"
  print ""
  print   sys.argv[0] +" - version : " + version
  print ""
  print ""
  sys.exit(0)

if options.time :
  nbr_days=int(options.time)

today=datetime.now().isoformat()
pastdate=datetime.today() - timedelta(days=nbr_days)
past_date=pastdate.isoformat()

def check_ct(dom):
	req = requests.get("https://crt.sh/?q=%."+ dom +"&output=json")
	if req.status_code != 200 :
		print("Server crt.sh is unavailable !!") 
		exit(1)
	
	jdata = json.loads('[{}]'.format(req.text.replace('}{', '},{')))
	#print jdata
	for (key,value) in enumerate(jdata):
	  cert=value['name_value']
	  date_emis=value['not_before']
	  issuer=value['issuer_name']
	  #print issuer
	  if date_emis > past_date :
	    try : 
	      bcn,acn=issuer.split("CN=")
	      #print value['name_value'] + " " + value['not_before']
	    except ValueError:
	      print "Oops!  No CN in issuer !"
	      acn=issuer
	    print cert + "\t" + date_emis + "\t" + acn

if options.domain :
  domain = options.domain
  check_ct(domain)
  sys.exit(0)
 
if options.filenamearg :
  filename=options.filenamearg
  with open(filename) as fp:
    for domain in fp:
      check_ct(domain.rstrip())
  sys.exit(0)  