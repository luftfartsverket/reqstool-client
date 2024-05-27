
FROM python:3.12.3-alpine

ENV PYTHONUNBUFFERED 1

LABEL org.opencontainers.image.title="reqstool"
LABEL org.opencontainers.image.description="This is custom Docker Image for reqstool."
LABEL org.opencontainers.image.authors="info@lfv.se"
LABEL org.opencontainers.image.vendor="LFV"
LABEL org.opencontainers.image.documentation="https://github.com/Luftfartsverket/reqstool-client/blob/main/README.md"
LABEL org.opencontainers.image.source="https://github.com/Luftfartsverket/reqstool-client"
LABEL org.opencontainers.image.url="https://github.com/Luftfartsverket/reqstool-client"

RUN pip install --no-cache-dir reqstool

