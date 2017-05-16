# https://en.wikipedia.org/wiki/M3U
# module to create m3u playlist from a list of filepaths

import os
import glob

dir = "C:\\Users\\Electron\\Music\\test_music_mp3"
print(dir)

for (path, subdirs, files) in os.walk(dir):
    os.chdir(path)
    if glob.glob("*.mp3") != []:
        _m3u = open(os.path.split(path)[1] + ".m3u", "w")
        for song in glob.glob("*.mp3"):
            # print(song)
            _m3u.write(song + "\n")
        _m3u.close()

print("done")