# buildbot-worker for nspv unix tests

# Provides a base Ubuntu (18.04) image with latest buildbot worker installed
# Based on official buildbot/buildbot-worker Dockerfile
# Installs basic deps to compile libnspv and run python tests
# Build env variables are set in .env file: UX_BUILDMASTER UX_BUILDMASTER_PORT UX_WORKERNAME UX_WORKERPASS

FROM        ubuntu:bionic
MAINTAINER  SirSevenG

ARG         DEBIAN_FRONTEND=noninteractive

# Install libnspv deps
RUN         apt-get update && \
            apt-get -y install -q \
            build-essential \
            pkg-config \
            libc6-dev \
            m4 \
            g++-multilib \
            autoconf \
            libtool \
            ncurses-dev \
            unzip \
            git \
            libffi-dev \
            libssl-dev \
            python3-setuptools \
            subversion \
            python-zmq \
            zlib1g-dev \
            wget \
            libcurl4-gnutls-dev \
            bsdmainutils \
            automake \
            curl \
            cmake \
            mingw-w64 \
            libevent-2.1-6 \
            libevent-pthreads-2.1-6 \
            libevent-dev \
            libsodium23 \
            libsodium-dev \
            libsodium-dev \
            python3-dev \
            python3-pip \
            libgnutls28-dev && \
            rm -rf /var/lib/apt/lists/* && \
            pip3 install --upgrade pip && \
            curl https://github.com/Yelp/dumb-init/releases/download/v1.2.1/dumb-init_1.2.1_amd64.deb -Lo /tmp/init.deb && \
            dpkg -i /tmp/init.deb && \
            # Install required python packages, and twisted
            pip --no-cache-dir install 'twisted[tls]' && \
            mkdir /buildbot && \
            useradd -ms /bin/bash buildbot

# Download buidbot-worker folder from official repo
RUN         svn checkout https://github.com/buildbot/buildbot/trunk/worker /usr/src/buildbot-worker
COPY        docker/buildbot.tac /buildbot/buildbot.tac

RUN         pip3 install /usr/src/buildbot-worker && \
            chown -R buildbot /buildbot

USER buildbot
WORKDIR /buildbot

CMD ["/usr/bin/dumb-init", "twistd", "--pidfile=", "-ny", "buildbot.tac"]
