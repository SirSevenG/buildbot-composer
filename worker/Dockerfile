# buildbot-worker for nspv unix tests

# Provides a base Ubuntu (18.04) image with latest buildbot worker installed
# Installs basic deps to compile libnspv and run python tests
# Build env variables are set in .env file: UX_BUILDMASTER UX_BUILDMASTER_PORT UX_WORKERNAME UX_WORKERPASS

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

USER buildbot
WORKDIR /buildbot

CMD ["/usr/bin/dumb-init", "twistd", "--pidfile=", "-ny", "buildbot.tac"]
