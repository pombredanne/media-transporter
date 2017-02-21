import os, subprocess
from . import TransportException
import config

class Storage():
    def __init__(self):
        self.share_path = self.locate_media_share()

    def locate_media_share(self):
        media_shares = config.media_shares
        for path in media_shares.split(','):
            if os.path.isdir(path):
                return path
            raise TransportException('[!] Media Share %s was not found, terminating...' % path, True)

    def get_volume_capacity(self):
        command = """df -H %s | tail -n1 | awk '{ print $5 " " $4 }'""" % self.share_path
        command_output = subprocess.check_output(command, shell=True)
        return command_output.split(' ')

    def capacity_reached(self):
        percentage_free, available_space = self.get_volume_capacity()
        percentage_free = int(percentage_free.replace('%',''))
        if percentage_free >= int(config.safe_capacity_percentage):
            return True
        return False
