FROM cgr.dev/chainguard/python:latest-dev as build

# Switch to root for package installation
USER root

# Install build dependencies
RUN apk add --no-cache \
    --repository=https://packages.wolfi.dev/os \
    build-base \
    libffi-dev \
    rust \
    pkgconf \
    linux-headers

# Create a virtualenv that we'll copy to the published image
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH="/app:$PYTHONPATH"

# Install dependencies first
RUN pip3 install setuptools-rust pyopenssl cryptography rns>=0.9.4 lxmf>=0.6.3 urwid>=2.6.16 qrcode

COPY . /app/
WORKDIR /app

# Install the package in development mode
RUN pip3 install -e .

# Use multi-stage build, as we don't need rust compilation on the final image
FROM cgr.dev/chainguard/python:latest-dev

LABEL org.opencontainers.image.documentation="https://github.com/markqvist/NomadNet#nomad-network-daemon-with-docker"

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED="yes"
ENV PYTHONPATH="/app:$PYTHONPATH"
COPY --from=build /opt/venv /opt/venv
COPY --from=build /app /app

# Create directories and set permissions
RUN mkdir -p /home/nonroot/.reticulum /home/nonroot/.nomadnetwork && \
    chown -R nonroot:nonroot /home/nonroot

USER nonroot
WORKDIR /home/nonroot

VOLUME /home/nonroot/.reticulum
VOLUME /home/nonroot/.nomadnetwork

ENTRYPOINT ["nomadnet"]
CMD ["--daemon"]
