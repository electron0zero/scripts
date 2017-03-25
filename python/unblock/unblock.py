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
from bs4 import BeautifulSoup
import requests
import re
import sys
from urllib.parse import urlparse

sys.setrecursionlimit(1500)


def getIP(hostname):
    print("Fetching IP Address for " + hostname)
    # domainname=google.com&ipaddress=127.0.0.1&findIP=+Find+IP+Address+
    payload = {'domainname': hostname, 'findIP': '+Find+IP+Address+'}
    # print(payload)
    r = requests.post("http://www.hcidata.info/host2ip.cgi", data=payload)
    r.keep_alive = False
    result = r.text.encode('utf-8')
    # print(result)
    soup = BeautifulSoup(result, 'lxml')
    # print(soup)
    preTag = str(soup.find_all('pre'))
    ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', preTag)
    # print(ip[0])
    return ip[0]


def isValidIP(ipaddress):
    # Found this on
    # http://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python
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
    # Found this on from
    # http://stackoverflow.com/questions/2532053/validate-a-hostname-string
    if len(hostname) > 255:
        return False
    if hostname[0].isdigit():
        return False
    if hostname[-1:] == ".":
        # strip exactly one dot from the right, if present
        hostname = hostname[:-1]
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

# Updates the Host File


def update(ipaddress, hostname):
    # linux host file location
    if 'linux' in sys.platform:
        filename = '/etc/hosts'
    # windwos host file location
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
    # windwos host file location
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
    # common URL that we don't want to add in host file
    # None is result from javascript:void(0) and we want to remove it
    common = [None, 'www.facebook.com', 'www.youtube.com', 'www.twitter.com', 'plus.google.com', 'www.google-analytics.com', 'apis.google.com',
              'ajax.googleapis.com', 'twitter.com', 'platform.twitter.com', 'p.twitter.com', 'platform.tumblr.com', 'github.com', 'www.github.com']
    hosts = []

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
            print(hostname, "is not a valid hostname.")
            continue
        if exists(hostname):
            # checks to see if the host name already exists in the host file
            # and exits if it does.
            print(hostname, 'already exists in the hostfile.')
            continue

        ipaddress = getIP(hostname)
        # print(ipaddress)
        # print(isValidIP(ipaddress))
        if not isValidIP(ipaddress):
            print(ipaddress, "is not a valid ipaddress.")
            continue
        # everything is OK update it in hostfile
        update(ipaddress, hostname)
        print("\"" + hostname + "\"" + " and ip address " +
              "\"" + ipaddress + "\"" + " is added to Hosts file")

    print("\nDone")


def main():
    args = sys.argv[1:]
    hostname = ''
    url = ''

    if len(args) != 2:
        print('usage: <filename> hostname url')
        sys.exit(1)

    hostname = args[0]
    url = args[1]
    # print(hostname)
    # print(validHostname(hostname))
    if not isValidHostname(hostname):
        # checks the host name to see if it's valid.
        print(hostname, "is not a valid hostname.")
        sys.exit(2)
    if exists(hostname):
        # checks to see if the host name already exists in the host file and
        # exits if it does.
        print(hostname, 'already exists in the hostfile.')
        # update all the extra hosts if some is missing
        updateHosts(hostname)
        sys.exit(2)

    ipaddress = getIP(hostname)

    # print(ipaddress)
    # print(isValidIP(ipaddress))
    if not isValidIP(ipaddress):
        print(ipaddress, "is not a valid ipaddress.")
        sys.exit(2)

    # everything is OK update it in hostfile
    update(ipaddress, hostname)
    print("\"" + hostname + "\"" + " and ip address " +
          "\"" + ipaddress + "\"" + " is added to Hosts file")
    # update all the extra hosts
    updateHosts(url)


if __name__ == '__main__':
    main()
