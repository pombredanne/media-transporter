import os
import shutil
import re
import glob
import subprocess
from . import Storage, Logger, TransportException
import config

flatten_list = lambda l: [item for sublist in l for item in sublist]


class MediaFile(Storage):

    def __init__(self, download_path, file_name, title):
        self.file_name = file_name
        self.title = re.sub(r'(\.|_){1,}', ' ', title)
        self.download_path = download_path
        self.has_video_extension = self.file_name.endswith(
            ('mkv', 'avi', 'mp4', 'mov'))

        if os.path.isdir('%s/%s' % (download_path, file_name)):
            os.chdir('%s/%s' % (download_path, file_name))
        Storage.__init__(self)

    def move_media(self):
        from . import TvFile, MovieFile

        if isinstance(self, MovieFile):
            Logger.log('[-] Movie %s wasn\'t found. Moving...' % self.title)
        elif isinstance(self, TvFile):
            Logger.log('[-] %s Season %s Episode %s wasn\'t found. Moving...' %
                       self.title, self.season, self.episode)
        shutil.move('%s/%s' % (self.download_path, self.file_name),
                    self.movie_root_path)

    def extract_media(self):
        from . import TvFile, MovieFile

        rar_files = glob.glob('*.rar')
        unrar_command = '%s x %s &>/dev/null' % (
            config.unrar_path, rar_files[0])
        try:
            destination_path = ''
            message = '[-] %s wasn\'t found. Extracting and moving...'
            if isinstance(self, TvFile):
                destination_path = self.tv_season_path
                Logger.log(message % '%s Season %s Episode %s' %
                           (self.title, self.season, self.episode))
            elif isinstance(self, MovieFile):
                destination_path = self.movie_root_path
                Logger.log(message % self.title)

            subprocess.check_output(unrar_command, shell=True)
            extracted_files = flatten_list([glob.glob(extension) for extension in [
                                           '*.mkv', '*.avi', '*.mp4', '*.mov']])
            for file in extracted_files:
                shutil.move(file, destination_path)
        except Exception as e:
            raise TransportException('[!] runtime error: %s.' % e, True)
