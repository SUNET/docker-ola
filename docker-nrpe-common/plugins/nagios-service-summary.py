#!/usr/bin/env python

import json
import sys
import nagiosplugin
import argparse
import requests
try:
   import requests_cache
   requests_cache.install_cache('nagios_status')
except ImportError as ex:
   pass

summary = dict()

class SetEncoder(json.JSONEncoder):
   def default(self, obj):
      if isinstance(obj, set):
         return list(obj)
      return json.JSONEncoder.default(self, obj)

_states = {'0': nagiosplugin.state.Ok,
           '1': nagiosplugin.state.Warn,
           '2': nagiosplugin.state.Critical,
           '3': nagiosplugin.state.Unknown}

class ServiceSummaryCheck(nagiosplugin.Resource):
   def __init__(self, service_name, status_urls):
      self.service_name = service_name
      self.status_urls = status_urls

   def probe(self):
      self.summary = dict()
      for status_url in self.status_urls:
         r = requests.get(status_url)
         if r.status_code == 200: 
            status = r.json()
            for host,status in status['content'].items():
               if self.service_name in status['services']:
                  current_state = _states[str(status['services'][self.service_name]['current_state'])]
                  self.summary.setdefault(current_state,set())
                  self.summary[current_state].add(host)
      for state,hosts in self.summary.items():
         yield nagiosplugin.Metric('#{} for {}'.format(state,self.service_name),len(hosts),context=self.service_name)

class ServiceSummary(nagiosplugin.Summary):
   def __init__(self, service_name):
      self.service_name = service_name

@nagiosplugin.guarded
def main():
   argp = argparse.ArgumentParser(description=__doc__)
   argp.add_argument('-w', '--warning', metavar='RANGE', default='', help='return warning if number of failed hosts is outside RANGE')
   argp.add_argument('-c', '--critical', metavar='RANGE', default='', help='return critical if number of failed hosts is outside RANGE')
   argp.add_argument('-n', '--service', metavar='NAME', default='Uptime', help='the service to summarize')
   argp.add_argument('-s', '--status', metavar='URI', type=str, action='append', help='<Required> status source')
   argp.add_argument('-v', '--verbose', action='count', default=0, help='increase output verbosity (use up to 3 times)')
   args = argp.parse_args()
   check = nagiosplugin.Check(ServiceSummaryCheck(args.service,args.status),
                              ServiceSummary(args.service),
                              nagiosplugin.ScalarContext(args.service, args.warning, args.critical))
   check.name = "{} summary".format(args.service)
   check.main(verbose=args.verbose)

if __name__ == '__main__':
   main()
