from bs4 import BeautifulSoup
import requests
import re
import sys
from urlparse import urlparse

def getIP(hostname):
    print("Fetching IP Address for "+ hostname)
    # domainname=google.com&ipaddress=127.0.0.1&findIP=+Find+IP+Address+
    payload = {'domainname': hostname,'findIP':'+Find+IP+Address+'}
    # print(payload)
    r = requests.post("http://www.hcidata.info/host2ip.cgi", data=payload)
    r.keep_alive = False
    result = r.text.encode('utf-8')
    # print(result)
    soup = BeautifulSoup(result, 'lxml')
    # print(soup)
    preTag = str(soup.find_all('pre'))
    ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', preTag )
    # print(ip[0])
    return ip[0]

def isValidIP(ipaddress):
    # Found this on http://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python
    parts = ipaddress.split(".")
    if len(parts) != 4:
        return False
    if ipaddress[-2:] == '.0': return False
    if ipaddress[-1] == '.': return False
    for item in parts:
        if not 0 <= int(item) <= 255:
            return False
    return True


def isValidHostname(hostname):
    # Found this on from http://stackoverflow.com/questions/2532053/validate-a-hostname-string
    if len(hostname) > 255:
        return False
    if hostname[0].isdigit(): return False
    if hostname[-1:] == ".":
        hostname = hostname[:-1] # strip exactly one dot from the right, if present
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

# Updates the Host File
def update(ipaddress, hostname):
    if 'linux' in sys.platform:
        filename = '/etc/hosts'
    else:
        filename = 'c:\windows\system32\drivers\etc\hosts'
    outputfile = open(filename, 'a')
    entry = "\n" + ipaddress + "\t" + hostname
    outputfile.writelines(entry)
    outputfile.close()


def exists(hostname):
    if 'linux' in sys.platform:
        filename = '/etc/hosts'
    else:
        filename = 'c:\windows\system32\drivers\etc\hosts'
    f = open(filename, 'r')
    hostfiledata = f.readlines()
    f.close()
    for item in hostfiledata:
        if hostname in item:
            return True
    return False

def getHosts(hostname):
    # common URL that we don't want to add in host file
    # None is resulves from javascript:void(0) and we want to remove it
    common = [ None, 'www.facebook.com', 'www.youtube.com', 'www.twitter.com', 'plus.google.com', 'www.google-analytics.com', 'apis.google.com', 'ajax.googleapis.com', 'twitter.com', 'platform.twitter.com', 'p.twitter.com', 'platform.tumblr.com']
    hosts = []

    url = "http://"+hostname

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

def updateHosts(hostname):
    hosts = getHosts(hostname)
    for hostname in hosts:
        ipaddress = ''
        if not isValidHostname(hostname):
            #checks the host name to see if it's valid.
            print(hostname, "is not a valid hostname.")
            continue
        if exists(hostname):
            #checks to see if the host name already exists in the host file and exits if it does.
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
        print("\""+hostname+"\"" + " and ip address " +"\""+ ipaddress +"\""+ " is added to Hosts file")

    print("\nDone")

def main():
    args = sys.argv[1:]
    hostname = ''

    if len(args) != 1 :
      print('usage: <filename> hostname')
      sys.exit(1)

    hostname = args[0]
    # print(hostname)
    # print(validHostname(hostname))
    if not isValidHostname(hostname):
        #checks the host name to see if it's valid.
        print(hostname, "is not a valid hostname.")
        sys.exit(2)
    if exists(hostname):
        #checks to see if the host name already exists in the host file and exits if it does.
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
    print("\""+hostname+"\"" + " and ip address " +"\""+ ipaddress +"\""+ " is added to Hosts file")
    # update all the extra hosts
    updateHosts(hostname)


if __name__ == '__main__':
    main()
