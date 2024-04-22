FROM ubuntu:latest
LABEL authors="hexa"

ENTRYPOINT ["top", "-b"]