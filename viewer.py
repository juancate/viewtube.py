# -*- coding: utf-8 -*-
#!/usr/bin/env python2

import time, os.path
from subprocess import Popen, PIPE

# function to get the video name base on its youtube url.
def get_file_name(url, youtube_dl_path=''):
  args = [youtube_dl_path + 'youtube-dl', '--get-filename',
          '-o', '"%(title)s.%(ext)s"', url]

  process = Popen(args, stdout=PIPE)
  name = process.communicate()[0][:-1]
  return name

# function to download and playback a youtube video
# TODO kill process when player is closed
def play_video(name, url, player_args, delay=5, youtube_dl_path=None):
  if os.path.isfile(name):
    player_args = player_args[:-5]
  else:
    print('Downloading...')
    if youtube_dl_path is not None:
      args_download = youtube_dl_path
    args_download += 'youtube-dl -q -o %s %s' % (name, url)

    log_download = file("/tmp/.log_youtube-dl", "w")
    download_process = Popen(args_download, shell=True,
                             stdout=log_download, stderr=log_download)

    time.sleep(delay) # waits while the download starts.

  log_player = file("/tmp/.log_simpleviewer", "w")
  player_process = Popen(player_args, shell=True,
                         stdout=log_player, stderr=log_player)

  if player_process.wait():
    player_process.terminate()

# main function
if __name__ == '__main__':
  from os import sys

  youtube_dl_path = '$HOME/bin/'
  video_name      = get_file_name(sys.argv[1], youtube_dl_path)
  video_name      = '"/tmp/' + video_name[1:]
  player_args     = 'mplayer %s.part' % video_name

  play_video(video_name, sys.argv[1], player_args, youtube_dl_path=youtube_dl_path)
