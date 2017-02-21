import os
from datetime import datetime
import config

script_path = '%s/../' % os.path.dirname(os.path.abspath(__file__))

class Logger():
    @staticmethod
    def log(text):
        dt = datetime.now()
        with open('%s/%s' % (script_path, config.logfile),'a') as fh:
            fh.write('[%s] %s\n' % (dt.strftime('%Y-%m-%d %H:%M:%S'),text))
        print '[%s] %s' % (dt.strftime('%Y-%m-%d %H:%M:%S'), text)
