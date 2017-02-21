#!/usr/bin/env python

import os, re, glob
import config
from classes import TransportException, Storage, TvFile, MovieFile

flatten_list = lambda l: [item for sublist in l for item in sublist]

if __name__ == '__main__':
    download_path = os.path.expanduser(config.download_path)
    os.chdir(download_path)

    storage = Storage()
    if storage.capacity_reached():
        raise TransportException('[!] Media share capacity reached, exiting...', True)

    categorized_files = {
        'tv': [],
        'movie': [],
    }

    files_to_check = []
    files_to_check.extend(flatten_list([glob.glob(extension) for extension in ['*.mkv','*.avi','*.mp4','*.mov']]))
    files_to_check.extend(filter(os.path.isdir, os.listdir(download_path)))
    for file in files_to_check:
        regex_tv = re.compile(r'%s' % config.regex_tv)
        regex_movie = re.compile(r'%s' % config.regex_movie)

        if regex_tv.findall(file):
            categorized_files['tv'].append({
                'path': file,
                'info': regex_tv.search(file).groups()
            })
        elif regex_movie.findall(file):
            categorized_files['movie'].append({
                'path': file,
                'info': regex_movie.search(file).groups()
            })

    for media_type, files in categorized_files.iteritems():
        if media_type == 'tv':
            for file_info in files:
                tv_obj = TvFile(download_path, file_info.get('path'), file_info.get('info'))
                tv_obj.prepare_destination()
                tv_obj.process()
        elif media_type == 'movie':
            for file_info in files:
                movie_obj = MovieFile(download_path, file_info.get('path'), file_info.get('info'))
                movie_obj.prepare_destination()
                movie_obj.process()
