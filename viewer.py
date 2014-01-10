#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os.path
import json
from subprocess import Popen, PIPE


def get_file_name(url, youtube_dl_path=''):
    """
    Get video file name.
    parameters: video url
    return: unicode string with the filename
    """
    args = youtube_dl_path + 'youtube-dl '
    args += '--get-filename -o "%(title)s.%(ext)s" ' + url
    args += ' --restrict-filenames'

    process = Popen(args, stdout=PIPE, shell=True)
    name = process.communicate()[0][:-1]

    return name.decode('unicode_escape')


def play_video(name, url, player_args, opt):
    """
    Download video and play it back.
    parameters: video name
                video url
                player args
                configuration options
    """
    download_process = None

    if os.path.isfile(name):
        player_args = player_args[:-6] + '"'
    else:
        print('Downloading...')
    download_args = opt['youtube_dl_path']
    download_args += 'youtube-dl -q -c -o "%s" -f %s %s' % \
                     (name, opt['quality'], url)

    download_process = Popen(download_args, shell=True)

    time.sleep(config['delay'])  # waits while the download starts.

    print('Playing: %s' % config['video'])
    player_process = Popen(player_args, shell=True, stdout=PIPE)

    if player_process.wait() is not None:
        if download_process is not None:
            download_process.terminate()


def load_config():
    """
    Load configuration file.
    """
    real_path = os.path.dirname(os.path.realpath(__file__))
    config = json.load(open(real_path + '/config.json'))

    if 'player_path' not in config:
        config['player_path'] = 'mplayer'
    if 'youtube_dl_path' not in config:
        config['youtube_dl_path'] = ''
    if 'download_path' not in config:
        config['download_path'] = '/tmp'
    if 'delay' not in config:
        config['delay'] = '5'
    config['delay'] = int(config['delay'])

    return config


# main function
if __name__ == '__main__':
    from os import sys

    config = load_config()

    video_name = get_file_name(sys.argv[1], config['youtube_dl_path'])
    config['video'] = video_name
    video_name = config['download_path'] + '/' + video_name
    player_args = '%s "%s.part"' % (config['player_path'], video_name)

    play_video(name=video_name, url=sys.argv[1],
               player_args=player_args, opt=config)
