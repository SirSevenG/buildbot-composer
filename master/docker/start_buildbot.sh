#!/bin/sh

# startup script for purely stateless master

# we download the config from an arbitrary curl accessible tar.gz file (which github can generate for us)

B=`pwd`

BUILDBOT_CONFIG_DIR=${BM_BUILDBOT_CONFIG_DIR:-config}
mkdir -p $B/$BUILDBOT_CONFIG_DIR
# if it ends with .tar.gz then its a tarball, else its directly the file

# copy the default buildbot.tac if not provided by the config
if [ ! -f $B/buildbot.tac ]
then
    cp /usr/src/buildbot/docker/buildbot.tac $B
fi

# Fixed buildbot master not start error in docker
rm -f $B/twistd.pid

# wait for db to start by trying to upgrade the master
until buildbot upgrade-master $B
do
    echo "Can't upgrade master yet. Waiting for database ready?"
    sleep 1
done

# we use exec so that twistd use the pid 1 of the container, and so that signals are properly forwarded
exec twistd -ny $B/buildbot.tac
