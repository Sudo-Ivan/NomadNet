FROM cgr.dev/chainguard/python:latest-dev AS build

USER root

RUN apk add --no-cache \
    --repository=https://packages.wolfi.dev/os \
    build-base \
    libffi-dev \
    rust \
    pkgconf \
    linux-headers

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH="/app"

RUN pip3 install setuptools-rust pyopenssl cryptography rns>=1.0.3 lxmf>=0.9.3 urwid>=2.6.16 qrcode

COPY . /app/
WORKDIR /app

RUN pip3 install -e .

RUN mkdir -p /home/nonroot/.reticulum /home/nonroot/.nomadnetwork && \
    chown -R 65532:65532 /home/nonroot && \
    chmod -R 755 /home/nonroot/.nomadnetwork

FROM cgr.dev/chainguard/python:latest

LABEL org.opencontainers.image.documentation="https://github.com/markqvist/NomadNet#nomad-network-daemon-with-docker"

COPY --from=build /opt/venv /opt/venv
COPY --from=build /app /app
COPY --from=build /home/nonroot /home/nonroot

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED="yes"
ENV PYTHONPATH="/app"

USER nonroot
WORKDIR /home/nonroot

VOLUME /home/nonroot/.reticulum
VOLUME /home/nonroot/.nomadnetwork

ENTRYPOINT ["/opt/venv/bin/nomadnet"]
CMD ["--daemon"]
