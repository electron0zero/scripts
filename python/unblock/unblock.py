import requests
from bs4 import BeautifulSoup
import os
import json
import re
import sys
from urllib.parse import urlparse

# https://stackoverflow.com/a/106223/5209755
regex_valid_hostname = r"^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
regex_valid_ip_address = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"


def getIP(hostname):
    print("Fetching IP Address for " + hostname)
    url = r"https://freegeoip.net/json/" + hostname
    response = requests.get(url)
    json_data = json.loads(response.text)
    ip = json_data.get("ip")
    return ip


def isValidIP(ipaddress):
    parts = ipaddress.split(".")
    if len(parts) != 4:
        return False
    if ipaddress[-2:] == '.0':
        return False
    if ipaddress[-1] == '.':
        return False
    for item in parts:
        if not 0 <= int(item) <= 255:
            return False
    return True


def isValidHostname(hostname):
    # Max len for Hostname is 255
    if len(hostname) > 255:
        return False
    allowed = re.compile(regex_valid_hostname, re.IGNORECASE | re.MULTILINE | re.UNICODE)
    return all(allowed.match(x) for x in hostname.split("."))


# Updates the Host File
def update(ipaddress, hostname):
    # linux host file location
    if 'linux' in sys.platform:
        filename = '/etc/hosts'
    # windows host file location
    elif 'win32' in sys.platform:
        filename = 'c:\windows\system32\drivers\etc\hosts'
    # macOS host file location
    elif 'darwin' in sys.platform:
        filename = '/etc/hosts'

    outputfile = open(filename, 'a')
    entry = "\n" + ipaddress + "\t" + hostname
    outputfile.writelines(entry)
    outputfile.close()


def exists(hostname):
    # linux host file location
    if 'linux' in sys.platform:
        filename = '/etc/hosts'
    # windows host file location
    elif 'win32' in sys.platform:
        filename = 'c:\windows\system32\drivers\etc\hosts'
    # macOS host file location
    elif 'darwin' in sys.platform:
        filename = '/etc/hosts'
    f = open(filename, 'r')
    hostfiledata = f.readlines()
    f.close()

    for item in hostfiledata:
        if hostname in item:
            return True
    return False


def getHosts(url):
    hosts = []
    # common is list of hostnames that we don't want to add in host file
    common = []

    print("\nFetching all extra domains for " + url + "\n")
    r = requests.get(url)
    r.keep_alive = False
    result = r.text.encode('utf-8')
    # print(result)
    soup = BeautifulSoup(result, 'lxml')
    # print(soup)

    href_tags = soup.find_all(href=True)
    for link in href_tags:
        href = link.get("href")
        hosts.append(urlparse(href).hostname)

    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "hostname.ignore"
    abs_file_path = os.path.join(script_dir, rel_path)

    with open(abs_file_path, 'r') as f:
        common = [line.strip() for line in f]

    common.append(None)  # None is result from javascript:void(0) and we want to ingore it

    # print(common)

    hosts = set(hosts)
    hosts = list(set(hosts) - set(common))
    # print(hosts)
    # for host in hosts:
    #     print(host)
    return hosts


def updateHosts(url):
    hosts = getHosts(url)
    for hostname in hosts:
        ipaddress = ''
        if not isValidHostname(hostname):
            # checks the host name to see if it's valid.
            print(hostname + "\tis not a valid hostname.")
            continue
        if exists(hostname):
            # checks to see if the host name already exists in the host file
            # and exits if it does.
            print(hostname, "\talready exists in the hostfile.")
            continue

        ipaddress = getIP(hostname)
        # print(ipaddress)
        # print(isValidIP(ipaddress))
        if not isValidIP(ipaddress):
            print(ipaddress, "\tis not a valid ipaddress.")
            continue
        # everything is OK update it in hostfile
        update(ipaddress, hostname)
        print("\"" + hostname + "\"" + " and ip address " +
              "\"" + ipaddress + "\"" + " is added to hostfile")
    print("\nDone")


def main():
    args = sys.argv[1:]

    if len(args) != 1:
        print('usage: unblock.py <url>')
        sys.exit(1)

    url = args[0]
    hostname = urlparse(url).hostname

    # print(hostname)
    # print(validHostname(hostname))
    if not isValidHostname(hostname):
        # checks the host name to see if it's valid.
        print(hostname, "\tis not a valid hostname.")
        sys.exit(2)
    if exists(hostname):
        # checks to see if the host name already exists in the host file and
        # exits if it does.
        print(hostname, "\talready exists in the hostfile.")
        # update all the extra hosts if some is missing
        updateHosts(url)
        sys.exit(2)

    ipaddress = getIP(hostname)

    # print(ipaddress)
    # print(isValidIP(ipaddress))
    if not isValidIP(ipaddress):
        print(ipaddress, "\tis not a valid ipaddress.")
        sys.exit(2)

    # everything is OK update it in hostfile
    update(ipaddress, hostname)
    print("\"" + hostname + "\"  " + "and ip address" +
          "  \"" + ipaddress + "\"  " + "is added to hostfile")
    # update all the extra hosts
    updateHosts(url)


if __name__ == '__main__':
    main()
