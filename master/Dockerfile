# buildbot-master for nspv

# Provides a base Ubuntu (18.04) image with latest buildbot installed
# Based on official buildbot container image, uses local master.cfg instead of downloading it
# Build env variables are set in .env file: UX_BUILDMASTER UX_BUILDMASTER_PORT UX_WORKERNAME UX_WORKERPASS

FROM        buildbot/buildbot-master:v2.3.1
MAINTAINER  SirSevenG

COPY docker/ /var/lib/buildbot
RUN chmod 700 -R /var/lib/buildbot/secrets

WORKDIR /var/lib/buildbot
CMD ["dumb-init", "/usr/src/buildbot/docker/start_buildbot.sh"]
