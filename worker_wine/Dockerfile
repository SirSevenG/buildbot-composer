# buildbot-worker for nspv windows tests

# Provides a base Ubuntu (18.04) image with latest buildbot worker installed
# Installs basic deps to compile libnspv and run python tests for windows(uner wine64)
# Build env variables are set in .env file: WN_BUILDMASTER WN_BUILDMASTER_PORT WN_WORKERNAME WN_WORKERPASS

FROM        buildbot:buildbot-worker
MAINTAINER  SirSevenG

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
            python \
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
            libgnutls28-dev

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

USER buildbot
WORKDIR /buildbot

CMD ["/usr/bin/dumb-init", "twistd", "--pidfile=", "-ny", "buildbot.tac"]
