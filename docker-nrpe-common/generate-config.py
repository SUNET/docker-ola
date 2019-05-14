#!/usr/bin/env python3

import sys
import yaml
import os

cfg = sys.argv[1]
ola_name = os.environ.get('OLA_NAME')
ola_hostname = os.environ.get('OLA_HOSTNAME')
ola_port = int(os.environ.get('OLA_PORT'))
nrpe_command = "check_nrpe_{}".format(name)

data = yaml.load(file(sys.argv[1],'r'))

with open(os.path.join("/etc/nrpe.d","{}_commands.cfg".format(name)),"w") as cfg:
         cfg.print("""
define command {
   command_name {}
   command_line /usr/lib/nagios/plugins/check_nrpe -H '$HOSTADDRESS$' -p {}
}
""".format(nrpe_command, ola_port)

if 'services' in data:
   for service in data['services']:
      cmd_name = (service.keys())[0]
      cmd_info = service[cmd_name]
      with open(os.path.join("/etc/nrpe.d","{}_services.cfg".format(name)),"w") as cfg:
         cfg.print("""
define service {
   host_name  {}
   check_command {}!{}
   display_name  {}
}
""".format(ola_hostname, nrpe_command, cmd_name, cmd_info['name'))
     with open(os.path.join("/etc/nrpe.d","{}_commands.cfg".format(name)),"w") as cfg:
         cfg.print("""
command[{}]={}
""".format(cmd_name, cmd_info['command']))
