# -*- coding: utf-8 -*-
#!/usr/bin/env python2

import time, os.path, json
from subprocess import Popen, PIPE

# function to get the video name base on its youtube url.
def get_file_name(url, youtube_dl_path=''):
  args = youtube_dl_path + 'youtube-dl '
  args += '--get-filename -o "%(title)s.%(ext)s" ' + url

  process = Popen(args, stdout=PIPE, shell=True)
  name = process.communicate()[0][:-1]
  return name

# function to download and playback a youtube video
def play_video(name, url, player_args, delay=5, opt=dict()):
  download_process = None

  if os.path.isfile(name):
    player_args = player_args[:-6] + '"'
  else:
    print('Downloading...')
    download_args = opt['youtube_dl_path']
    download_args += 'youtube-dl -q -c -o "%s" -f %s %s' % (name, opt['quality'], url)

    download_process = Popen(download_args, shell=True)

    time.sleep(delay) # waits while the download starts.

  player_process = Popen(player_args, shell=True)

  if player_process.wait() is not None:
    if download_process is not None:
      download_process.terminate()

# load configuration file
def load_config():
  config = json.load(open('config.json'))

  if 'player_path' not in config:
    config['player_path'] = 'mplayer'
  if 'youtube_dl_path' not in config:
    config['youtube_dl_path'] = ''
  if 'download_path' not in config:
    config['download_path'] = '/tmp'

  return config


# main function
if __name__ == '__main__':
  from os import sys

  config = load_config()

  video_name  = get_file_name(sys.argv[1], config['youtube_dl_path'])
  video_name  = config['download_path'] + '/' + video_name
  player_args = '%s "%s.part"' % (config['player_path'], video_name)

  play_video(name=video_name, url=sys.argv[1], player_args=player_args, opt=config)
