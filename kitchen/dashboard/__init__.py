"""Log settings for the"""
from logbook import MonitoringFileHandler

from kitchen.settings import LOG_FILE, DEBUG


file_log_handler = MonitoringFileHandler(LOG_FILE, bubble=DEBUG)
file_log_handler.push_application()
