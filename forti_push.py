#!/usr/bin/env python
import requests
import sys
import json

requests.packages.urllib3.disable_warnings()


class Fortigate(object):

    def __init__(self):
        self.fgt = "1.1.1.1" #IP or Hostname FortiGate
        self.token = "xxxxxxxxxxxxxxxxxx" #API token

        self.host = sys.argv[1]
        self.group = "BadIPList" #Address Group Name

        self.url = "https://" + self.fgt
        self.headers = {"Authorization": "Bearer " + self.token}
        self.verify = False

    def get(self, type):
        if type == 'address':
            object = self.host
        elif type == 'addrgrp':
            object = self.group

        res = requests.get(self.url + '/api/v2/cmdb/firewall/' + type + "/" + object, headers=self.headers,
                           verify=self.verify)
        return res

    def add_host(self):
        data = {'name': self.host, 'type': "ipmask",'subnet': self.host + " 255.255.255.255"}
        res = requests.post(self.url + '/api/v2/cmdb/firewall/address/', headers=self.headers, data=json.dumps(data),
                            verify=self.verify)
        return res

    def add_group(self):
        data = {'name': "BadIPList", 'member': [{'name': self.host}]}
        res = requests.post(self.url + '/api/v2/cmdb/firewall/addrgrp/', headers=self.headers, data=json.dumps(data),
                            verify=self.verify)
        return res

    def edit_group(self, members):
        data = {'member': members}
        res = requests.put(self.url + '/api/v2/cmdb/firewall/addrgrp/'+ self.group + '/', headers=self.headers,
                           data=json.dumps(data), verify=self.verify)
        return res


if __name__ == "__main__":
    fgt = Fortigate()
    check_host = fgt.get("address")

    if check_host.status_code != 200:
        print("Address does not exist")
        add_host = fgt.add_host()
        if add_host.status_code != 200:
            print("ERROR: Could not add host to FortiGate")
            sys.exit(1)
        print("Successfully added address")
    elif check_host.status_code == 200:
        print("Address exist already")
    else:
        print("Something went wrong.")
        sys.exit(1)

    check_group = fgt.get("addrgrp")
    if check_group.status_code == 200:
        print("Address Group exist already")

        try:
            rjson = check_group.json()["results"]
        except Exception as e:
            print("Could not decode JSON data in HTTP response " + e)
            sys.exit(1)

        for line in rjson:
            members = line["member"]
        for line in members:
            if fgt.host in line["name"]:
                print("Host in group already")
                sys.exit(1)
            else:
                print("Address is not member of this group")
                members.append({'q_origin_key': fgt.host, 'name': fgt.host})
                edit_group = fgt.edit_group(members)
                if edit_group.status_code == 200:
                    print("Address got added to this group")
                    sys.exit(1)

    elif check_group.status_code != 200:
        print("Address Group does not exist")
        create_group = fgt.add_group()
        if create_group.status_code != 200:
            print("ERROR: Could not add group to FortiGate")
        print("Successfully created address group")
        sys.exit(1)

    else:
        print("Something went wrong.")
        sys.exit(1)