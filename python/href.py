from bs4 import BeautifulSoup
import requests
import re
import sys
from urlparse import urlparse

# common URL that we don't want to add in host file
# None is resulves from javascript:void(0) and we want to remove it
common = [ None, 'www.facebook.com', 'www.youtube.com', 'www.twitter.com', 'plus.google.com', 'www.google-analytics.com', 'apis.google.com', 'ajax.googleapis.com', 'twitter.com', 'platform.twitter.com', 'p.twitter.com', 'platform.tumblr.com']
hosts = []

hostname = "www.pornhub.com"
url = "http://"+hostname
print("URL : " + url)
r = requests.get(url)
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
for host in hosts:
    print(host)
