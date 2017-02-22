import os
from . import MediaFile, Logger
import config


class MovieFile(MediaFile):

    def __init__(self, download_path, file_name, movie_info):
        title, year, resolution = movie_info
        MediaFile.__init__(self, download_path, file_name, title)

    def prepare_destination(self):
        self.movie_root_path = config.share_movie_root_path % (
            self.share_path, self.title)

        if os.path.isdir(self.movie_root_path):
            if self.capacity_reached():
                Logger.log(
                    '[!] Capacity reached. Skipping adding movie %s.' % self.title)
            else:
                if not os.path.isdir(self.movie_root_path):
                    Logger.log('[+] Adding Movie: %s' % self.title)
                    os.mkdir(self.movie_root_path)

    def process(self):
        existing_movie = os.listdir(self.movie_root_path)
        if not [movie for movie in existing_movie if self.title in movie]:
            if self.has_video_extension:
                self.move_media()
            else:
                self.extract_media()
