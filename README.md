# monitor-ct

This python script query the COMODO web server crt.sh to request the last certificate (from 7 days by default) generate for a domain or a list of domain (specify in a texte file).

https://github.com/zebux/monitor-ct/blob/master/monitor-ct.py

-------
 
Useful command lines

List, the last 7 days, generated certificate for the domain comodo.com
$ ./monitor-ct.py -d comodo.com

List all generated certificates since 2 days from the domain in the file domain.txt 
$ ./monitor-ct.py -f domain.txt -t 2