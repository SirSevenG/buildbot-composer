# buildbot-worker for nspv windows tests

# Provides a base Ubuntu (18.04) image with latest buildbot worker installed
# Based on official buildbot/buildbot-worker Dockerfile
# Installs basic deps to compile libnspv and run python tests for windows(uner wine64)
# Build env variables are set in .env file: WN_BUILDMASTER WN_BUILDMASTER_PORT WN_WORKERNAME WN_WORKERPASS

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
            python3-pip \
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
            python3-dev \
            python3-pip \
            libgnutls28-dev && \
            rm -rf /var/lib/apt/lists/* && \
            pip3 install --upgrade pip  && \
            curl https://github.com/Yelp/dumb-init/releases/download/v1.2.1/dumb-init_1.2.1_amd64.deb -Lo /tmp/init.deb && \
            dpkg -i /tmp/init.deb && \
            # Install required python packages, and twisted
            pip --no-cache-dir install 'twisted[tls]' && \
            mkdir /buildbot && \
            useradd -ms /bin/bash buildbot

# Install wine and deps to run win app
RUN         dpkg --add-architecture i386 && \
            apt-get update && \
            apt-get -y install -q software-properties-common && \
            wget -q https://dl.winehq.org/wine-builds/winehq.key && \
            apt-key add ./winehq.key  && \
            apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ bionic main'  && \
            apt-get update && \
            apt-get -y install --install-recommends -q winehq-stable \
            mono-complete &&\
            wget -q http://dl.winehq.org/wine/wine-gecko/2.47/wine_gecko-2.47-x86_64.msi && \
            wine msiexec /i wine_gecko-2.47-x86_64.msi

# Download buidbot-worker folder from official repo
RUN         svn checkout https://github.com/buildbot/buildbot/trunk/worker /usr/src/buildbot-worker
COPY        docker/buildbot.tac /buildbot/buildbot.tac

RUN         pip3 install /usr/src/buildbot-worker && \
            chown -R buildbot /buildbot

USER buildbot
WORKDIR /buildbot

CMD ["/usr/bin/dumb-init", "twistd", "--pidfile=", "-ny", "buildbot.tac"]
