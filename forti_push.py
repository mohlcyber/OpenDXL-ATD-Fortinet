#!/usr/bin/env python
import requests
import argparse
import sys
import json
from pprint import pprint

fgt_ip = "ip address"
user = "username"
pw = "password"

class FGT(object):
    def __init__(self, host):
        self.host = host
        self.url_prefix = "https://" + self.host

    def update_csrf(self):
        # retrieve server csrf and update session's headers
        for cookie in self.session.cookies:
            if cookie.name == "ccsrftoken":
                csrftoken = cookie.value[1:-1]  # token stored as a list
                self.session.headers.update({"X-CSRFTOKEN": csrftoken})

    def login(self, name="admin", key="", csrf=True):
        self.logout()

        self.session = requests.session()
        url = self.url_prefix + "/logincheck"
        try:
            res = self.session.post(
                url,
                data="username=" + name + "&secretkey=" + key,
                verify=False)
            print "LOGIN successful"
        except requests.exceptions.RequestException as e:
            print(e)
            print "LOGIN failed"
            exit()

        if res.text.find("error") != -1:
            # found some error in the response, consider login failed
            print "LOGIN failed"
            return False

        if csrf:
            self.update_csrf()
        return True

    def logout(self):
        if hasattr(self, "session"):
            url = self.url_prefix + "/logout"
            self.session.post(url)
            print "LOGOUT successful"

    def get(self, url, **options):
        url = self.url_prefix + url
        try:
            res = self.session.get(
                url,
                params=options.get("params"))
        except requests.exceptions.RequestException as e:
            print(e)
            exit()
        return res

    def post(self, url, override=None, **options):
        url = self.url_prefix + url
        data = options.get("data") if options.get("data") else None

        # override session's HTTP method if needed
        if override:
            self.session.headers.update({"X-HTTP-Method-Override": override})
        try:
            res = self.session.post(
                url,
                params=options.get("params"),
                data=json.dumps(data),
                files=options.get("files"))
        except requests.exceptions.RequestException as e:
            print(e)
            exit()

        # restore original session
        if override:
            del self.session.headers["X-HTTP-Method-Override"]
        return res

    def put(self, url, **options):
        url = self.url_prefix + url
        data = options.get("data") if options.get("data") else None
        try:
            res = self.session.put(
                url,
                params=options.get("params"),
                data=json.dumps(data),
                files=options.get("files"))
        except requests.exceptions.RequestException as e:
            print(e)
            exit()
        return res


def get_command(type, objname):
    res = fgt.get(
        url="/api/v2/cmdb/firewall/" + type + "/" + objname)
    return res

def create_host(host):
    data = {'name': host, 'type': "ipmask",'subnet': host + " 255.255.255.255"}
    res = fgt.post(
        url="/api/v2/cmdb/firewall/address/",
        data=data)

def create_group(member):
    data = {'name':"BadIPList", 'member': [{'name':member}]}
    res = fgt.post(
        url="/api/v2/cmdb/firewall/addrgrp/",
        data=data)
    return res

def edit_group(members):
    data = {'member': members}
    res = fgt.put(
        url="/api/v2/cmdb/firewall/addrgrp/BadIPList/",
        data = data)
    return res

def get_json(response):
    try:
        rjson = response.json()
    except UnicodeDecodeError as e:
        print "Cannot decode json data in HTTP response"
        return False
    except:
        e = sys.exc_info()[0]
        #print(e)
        return False
    else:
        return rjson

def check_response(res):
    rjson = get_json(res)
    #pprint(rjson)
    if not rjson:
        #print "fail to retrieve JSON response"
        pass
    else:
        status = rjson["http_status"]
        if status == 200:
            return status
            #print "200 successful request"
            pass
        elif status == 400:
            #print "400 Invalid request format"
            pass
        elif status == 403:
            #print "403 Permission denied"
            pass
        elif status == 404:
            #print "404 None existing resource"
            pass
        elif status == 405:
            #print "405 Unsupported method"
            pass
        elif status == 424:
            #print "424 Dependency error"
            pass
        elif status == 500:
            #print "500 Internal server error"
            pass
        else:
            #print status, "Unknown error"
            pass


if __name__ == "__main__":
    fgt = FGT(fgt_ip)
    fgt.login(user,pw)

    host = sys.argv[1]

    # Check If Host already exist if not create new Host
    res = get_command("address",host)
    status = check_response(res)
    if status == 200:
        print "Host exist already"

        # Check If Group exist if not create new Group
        res = get_command("addrgrp","BadIPList")
        status = check_response(res)
        if status == 200:
            print "Group exist already"

            # Get the members of the group
            res = get_command("addrgrp","BadIPList")
            rjson = get_json(res)["results"]
            for line in rjson:
                members = line["member"]
            for line in members:
                if host in line["name"]:
                    print "Host in group already"
                    exit()

            print "Host is not in group"
            members.append({'q_origin_key': host,'name': host})

            res = edit_group(members)
            status = check_response(res)
            print "User got added to the group"
        else:
            print "Group does not exist"
            res = create_group(host)
            status = check_response(res)
            print "Group got created"

    else:
        # Create new host
        print "Host does not exist"
        res = create_host(host)
        status = check_response(res)
        print "New Host got created"

        # Check if group exist if not create new group
        res = get_command("addrgrp","BadIPList")
        status = check_response(res)
        if status == 200:
            print "Group exist already"
            # Get the members of the group
            res = get_command("addrgrp","BadIPList")
            rjson = get_json(res)["results"]
            for line in rjson:
                members = line["member"]
            for line in members:
                if host in line["name"]:
                    print "Host in group already"
                    exit()

            print "Host is not in group"
            members.append({'q_origin_key': host,'name': host})

            res = edit_group(members)
            status = check_response(res)
            print "Host got added to the group"

        else:
            print "Group does not exist"
            res = create_group(host)
            status = check_response(res)
            print "Group got created"

    fgt.logout()
