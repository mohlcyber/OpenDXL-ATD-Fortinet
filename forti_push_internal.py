#!/usr/bin/env python3
# Written by mohlcyber v.0.1 - inspired by SelR4c
# This script is only for Internal IP Addresses not External IP Addresses

import sys
import requests
import json

requests.packages.urllib3.disable_warnings()

FORTINET_IP = '1.1.1.1'
FORTINET_PORT = '443'
FORTINET_TOKEN = 'token'
FORTINET_VDOM = 'root'


class Fortigate():

    def __init__(self):
        self.ip = FORTINET_IP
        self.port = FORTINET_PORT
        self.token = FORTINET_TOKEN
        self.vdom = FORTINET_VDOM

        self.url = 'https://{0}:{1}'.format(self.ip, self.port)
        self.headers = {'Authorization': 'Bearer ' + self.token}
        self.verify = False

    def quarantine_system(self, host):
        payload = {
            'ip_addresses': [host],
            'expiry': 0
        }

        res = requests.post(self.url + '/api/v2/monitor/user/banned/add_users', headers=self.headers,
                            data=json.dumps(payload), params={'vdom': self.vdom}, verify=self.verify)

        if res.status_code == 200:
            print('SUCCESS: Successful quarantined IP address {0}.'.format(host))
        else:
            print('ERROR: Something went wrong during the quarantine. Error: {0} {1}'
                  .format(str(res.status_code), str(res.text)))


if __name__ == "__main__":
    fgt = Fortigate()
    fgt.quarantine_system(sys.argv[1])