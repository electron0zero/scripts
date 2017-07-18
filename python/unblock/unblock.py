'''
NOTE : if a website is down for you make sure that it's doesn't have a entry in your host file
you will run into this case if a website changes it's IP, in that case that website will be down for you.
remove it from host file and unblock again.

HOW IT WORKS : see this video to understand it's working https://www.youtube.com/watch?v=zRysni9ND2w

Dependencies : lxml, BeautifulSoup4, requests
install by running `pip install BeautifulSoup4 requests lxml`
for windows users if lxml install fails get wheel from [this website](http://www.lfd.uci.edu/~gohlke/pythonlibs/) and install

Usage : python unblock.py <hostname>

A python Script to add stuff in hosts file helpful if your network blocks stuff by
DNS requests(like OpenDNS) and also block other DNS servers like Google public DNS

NOTE : it can only add hostname that are in homepage of website if you can't see anything on
other page of site that's not working, then look into console and see which hostname is
getting 404 or 403 then get that hostname and unblock that hostname also

python 3 compatible
Change 'urllib.parse'  in import statement to 'urlparse' if using python < 2.7.11
because urlparse module was renamed to urllib.parse in python 2.7.11
'''
import requests
from bs4 import BeautifulSoup
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

    with open('hostname.ignore', 'r') as f:
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
