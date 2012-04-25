"""Celery tasks for the dashboard app"""
import os
from datetime import timedelta
from subprocess import Popen, PIPE
import logging

from celery.task import PeriodicTask

from kitchen.settings import REPO, REPO_BASE_PATH
from kitchen.dashboard import chef

log = logging.getLogger(__name__)


class SyncRepo(PeriodicTask):
    """A Periodic Task that syncs the git kitchen repository"""
    run_every = timedelta(seconds=REPO['SYNC_SCHEDULE'])
    REPO_ROOT = os.path.join(REPO_BASE_PATH, REPO['NAME'])

    def run(self, **kwargs):
        """Task execution"""
        log.info("Synching repo")
        if os.path.exists(self.REPO_ROOT):
            self._update()
        else:
            self._clone()

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
