from celery.task import PeriodicTask
from datetime import timedelta, datetime
from settings import REPO_SYNC_SCHEDULE


class SyncRepo(PeriodicTask):
    run_every = timedelta(seconds=REPO_SYNC_SCHEDULE)

    def run(self, **kwargs):
        print "I am here! ({0})".format(str(datetime.now()))
