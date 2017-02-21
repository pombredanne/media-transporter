import sys
from . import Logger

class TransportException(Exception):
    def __init__(self, message, exit=False):
        super(TransportException, self).__init__(message)
        Logger.log(message)
        if exit:
            sys.exit(1)
