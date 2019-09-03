import fnmatch
import os
import sys

from twisted.application import service
from twisted.python.log import FileLogObserver
from twisted.python.log import ILogObserver

from buildbot_worker.bot import Worker

# setup worker
basedir = os.environ.get("BUILDBOT_BASEDIR",
                         os.path.abspath(os.path.dirname(__file__)))
application = service.Application('buildbot-worker')


application.setComponent(ILogObserver, FileLogObserver(sys.stdout).emit)
# and worker on the same process!
buildmaster_host = os.environ.get("WN_BUILDMASTER")
port = int(os.environ.get("WN_BUILDMASTER_PORT"))
workername = os.environ.get("WN_WORKERNAME")
passwd = os.environ.get("WN_WORKERPASS")

# delete the password from the environ so that it is not leaked in the log
blacklist = os.environ.get("WORKER_ENVIRONMENT_BLACKLIST", "WN_WORKERPASS").split()
for name in list(os.environ.keys()):
    for toremove in blacklist:
        if fnmatch.fnmatch(name, toremove):
            del os.environ[name]

keepalive = 600
umask = None
maxdelay = 300
allow_shutdown = None
maxretries = 10

s = Worker(buildmaster_host, port, workername, passwd, basedir,
           keepalive, umask=umask, maxdelay=maxdelay,
           allow_shutdown=allow_shutdown, maxRetries=maxretries)
s.setServiceParent(application)
