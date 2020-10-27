ARG BUILD_FROM=hassioaddons/base:7.2.0
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

# Copy root filesystem
COPY rootfs /

# Setup base
RUN apk add --no-cache \
    python3 \
    py3-boto3@edge \
    py3-watchdog \
    py3-requests

# Build arguments
ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_REF
ARG BUILD_VERSION

# Labels
LABEL \
    io.hass.name="FTP To S3" \
    io.hass.description="Backup to S3 files uploaded via FTP" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION} \
    maintainer="iLyas Bakouch <isbkch@gmail.com>" \
    org.opencontainers.image.title="FTP To S3" \
    org.opencontainers.image.description="Backup to S3 files uploaded via FTP" \
    org.opencontainers.image.vendor="Home Assistant Community Add-ons" \
    org.opencontainers.image.authors="iLyas bakouch <isbkch@gmail.com>" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.url="https://github.com/isbkch/hass-addons" \
    org.opencontainers.image.source="https://github.com/isbkch/hass-addons" \
    org.opencontainers.image.documentation="https://github.com/hass-addons/ftp-to-S3/blob/master/README.md" \
    org.opencontainers.image.created=${BUILD_DATE} \
    org.opencontainers.image.revision=${BUILD_REF} \
    org.opencontainers.image.version=${BUILD_VERSION}