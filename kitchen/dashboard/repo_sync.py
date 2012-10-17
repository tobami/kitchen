"""Repo sync module"""
import os
from datetime import timedelta
from subprocess import Popen, PIPE
from logbook import Logger, MonitoringFileHandler

import sys
path = os.path.dirname(os.path.dirname(
    os.path.abspath(os.path.dirname(__file__).replace('\\', '/'))))
sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'kitchen.settings'

from kitchen.settings import (REPO, REPO_BASE_PATH, SYNCDATE_FILE, LOG_FILE,
                              DEBUG)
from kitchen.dashboard import chef

file_log_handler = MonitoringFileHandler(LOG_FILE, bubble=DEBUG)
file_log_handler.push_application()
log = Logger("kitchen.sync")


class SyncRepo():
    """A Task that syncs the git kitchen repository"""
    REPO_ROOT = os.path.join(REPO_BASE_PATH, REPO['NAME'])

    def run(self):
        """Syncs the git repository"""
        log.debug("Synching repo")
        if os.path.exists(self.REPO_ROOT):
            self._update()
        else:
            self._clone()
        self._set_repo_sync_date()

    def _update(self):
        """Do a 'git pull'"""
        cmd = ['git', 'pull']
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, cwd=self.REPO_ROOT)
        log.info("Updating repo")
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            log.error("git pull returned {0}: {0}".format(
                      p.returncode, stderr))
        else:
            chef.build_node_data_bag()

    def _clone(self):
        """Clone a git repository"""
        if not os.path.exists(REPO_BASE_PATH):
            os.makedirs(REPO_BASE_PATH)
        cmd = ['git', 'clone', '--depth', '1', REPO['URL'], REPO['NAME']]
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, cwd=REPO_BASE_PATH)
        log.info('Cloning Git repo {0}'.format(REPO['URL']))
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            log.error("{0} returned {1}: {2}".format(
                      " ".join(cmd), p.returncode, stderr))
        else:
            chef.build_node_data_bag()

    def _set_repo_sync_date(self):
        """Sets the modified date of a file, which will be the sync date"""
        with file(SYNCDATE_FILE, 'a'):
            os.utime(SYNCDATE_FILE, None)


if __name__ == "__main__":
    sr = SyncRepo()
    sr.run()
