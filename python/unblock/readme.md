## Unblock stuff that is blocked by censoring DNS requests and public DNS is also not allowed on your network.

A python Script to add stuff in hosts file, helpful if your network blocks stuff by
DNS requests(like OpenDNS) and also block other DNS servers like Google public DNS

NOTE : if a website is down for you make sure that it's doesn't have a entry in your host file
you will run into this case if a website changes it's IP, in that case that website will be down for you.
remove it from host file and unblock again.

- check if a website is down just for you http://downforeveryoneorjustme.com/
- if http://freegeoip.net/ is blocked by your network, this script will not work

If you do not want a website to get added to your hostfile add it to `hostname.ignore` file


#### Python 3 compatible
Change `urllib.parse`  in `import` statement to `urlparse` if using `python < 2.7.11` because `urlparse` module was renamed to `urllib.parse` in `python 2.7.11`

#HOW IT WORKS
see this video to understand it's working https://www.youtube.com/watch?v=zRysni9ND2w
