#!/usr/bin/env python3

import sys
import yaml
import os

cfg = sys.argv[1]
ola_hostname = os.environ.get('OLA_HOSTNAME')
ola_port = int(os.environ.get('OLA_PORT'))

with open(sys.argv[1],'r') as cfg:
   data = yaml.load(cfg)

ola_name = data['name']
nrpe_command = "check_nrpe_{}".format(ola_name)

with open(os.path.join("/etc/nagios3/conf.d","{}_commands.cfg".format(ola_name)),"w") as cfg:
   cfg.write("""
define command {{
   command_name {}
   command_line /usr/lib/nagios/plugins/check_nrpe -H '$HOSTADDRESS$' -p {}
}}
""".format(nrpe_command, ola_port))

if 'services' in data:
   with open(os.path.join("/etc/nagios3/conf.d","{}_services.cfg".format(ola_name)),"w") as cfg:
      for service in data['services']:
         cmd_name = list(service.keys())[0]
         cmd_info = service[cmd_name]
         cfg.write("""
define service {{
   host_name     {}
   check_command {}!{}
   display_name  "{}"
}}
""".format(ola_hostname, nrpe_command, cmd_name, cmd_info['name']))

   with open(os.path.join("/etc/nrpe.d","{}.cfg".format(ola_name)),"w") as cfg:
      for service in data['services']:
         cmd_name = list(service.keys())[0]
         cmd_info = service[cmd_name]
         cfg.write("""
command[{}]="{}"
""".format(cmd_name, cmd_info['command']))
