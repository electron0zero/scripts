import requests
import shutil
from urllib.parse import urlparse
from os.path import splitext, basename, join
# file of readme urls
urls_file = open('urls.txt')
basepath = "..\\_includes\\readme"

for line in urls_file:
    # clean up filename and url
    parsed = urlparse(line)
    filename = parsed.path[1:]
    filename = filename.replace('/', '-')
    filename = filename.lower()
    filepath = join(basepath, filename)
    filepath = filepath.strip('\n')
    url = line.strip('\n')
    print("Getting file from URL: {}".format(url))
    print("Fetching and saving file at: {}".format(filepath))
    outfile = open(filepath, 'wb')
    resp = requests.get(url, stream=True)
    print("Staus code: {}".format(resp.status_code))
    if resp.status_code == 200:
        resp.raw.decode_content = True
        shutil.copyfileobj(resp.raw, outfile)
        print("Done")