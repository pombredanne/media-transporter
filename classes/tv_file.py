import os
import config
from . import Logger, MediaFile


class TvFile(MediaFile):

    def __init__(self, download_path, file_name, show_info):
        title, episode_id, season, episode = show_info
        self.episode_id = episode_id
        self.season = int(season)
        self.episode = int(episode)
        MediaFile.__init__(self, download_path, file_name, title)

    def prepare_destination(self):
        self.tv_root_path = config.share_tv_root_path % (
            self.share_path, self.title)
        self.tv_season_path = config.share_tv_season_path % (
            self.share_path, self.title, self.season)

        if os.path.isdir(self.tv_root_path):
            if self.capacity_reached():
                Logger.log('[!] Capacity reached. Skipping adding Season %s of %s.' % (
                    self.season, self.title))
            else:
                if not os.path.isdir(self.tv_season_path):
                    Logger.log('[+] Creating folder for Season %s of %s' %
                               (self.season, self.title))
                    os.mkdir(self.tv_season_path)
        else:
            if self.capacity_reached():
                Logger.log(
                    '[!] Capacity reached. Skipping adding show %s.' % self.title)
            else:
                Logger.log('[+] Adding TV Show: %s' % self.title)
                os.makedirs(self.tv_season_path)

    def process(self):
        existing_episodes = os.listdir(self.tv_season_path)
        if not [episode for episode in existing_episodes if self.episode_id in episode]:
            if self.has_video_extension:
                self.move_media()
            else:
                self.extract_media()
