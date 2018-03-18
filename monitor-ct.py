#!/usr/bin/python
# -*- coding: utf-8 -*-

'''

	@ author : Eric BEAULIEU <zebux@zebux.org>
	@copyright:  AGPLv3
             http://www.gnu.org/licenses/agpl.html

'''

import requests
import sys
import json
from datetime import datetime, timedelta



version = "v0.1"
nbr_days= 7
 
if len (sys.argv) < 2:     
  print "usage: " + sys.argv[0] + " [domains to check]"
  sys.exit(1)
 
if "-t" in sys.argv[1]:
  nbr_days=int(sys.argv[2])

today=datetime.now().isoformat()
pastdate=datetime.today() - timedelta(days=nbr_days)
past_date=pastdate.isoformat()
#print today
#print past_date
#print len(sys.argv)


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
	  #print value['name_value'] + " " + value['not_before']
	  if date_emis > past_date :
	    print cert + "\t" + date_emis + "\t" + issuer

if "-h" in sys.argv or "--help" in sys.argv:
  print "usage : "+sys.argv[0]+ " [-d] domain"
  print ""
  print "This script monitor certificat transparency from a domain"
  print ""
  print "Optional arguments:"
  print "   -h, --help    show this help message and exit"
  print "   -v, --version show version."
  print "   -f <filename>, Mass domain monitor option. File with one line per domain."
  print "   -t <days number>, Check certificat issue since <days number> days - default 7 days "
  sys.exit(0)

if "-v" in sys.argv or "--version" in sys.argv:
  print ""
  print ""
  print "This script monitor certificat transparency from a domain"
  print ""
  print " sys.argv[0] - version : " + version
  print ""
  print ""
  sys.exit(0)
  
if "-d" in sys.argv[1] :
  domain = sys.argv[2]
  check_ct(domain)
  sys.exit(0)

if len (sys.argv) == 5:
	if "-d" in sys.argv[3] :
	  domain = sys.argv[4]
	  check_ct(domain)
	  sys.exit(0)
	if "-f" in sys.argv[3]:
		filename=sys.argv[4]
		with open(filename) as fp:
			for domain in fp:
				check_ct(domain.rstrip())
	sys.exit(0)

if "-f" in sys.argv[1]:
  filename=sys.argv[2]
  with open(filename) as fp:
    for domain in fp:
      check_ct(domain.rstrip())
  sys.exit(0)



