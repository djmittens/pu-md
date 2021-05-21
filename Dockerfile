FROM alpine:latest

RUN sh -c 'echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories'
RUN apk update
RUN apk add --no-cache python3
RUN apk add --no-cache java-jre
RUN apk add --no-cache ripgrep
RUN apk add --no-cache fontconfig
RUN apk add --no-cache ttf-dejavu
RUN apk add --no-cache libxrender
RUN apk add --no-cache libxtst
RUN apk add --no-cache libxi
RUN apk add --no-cache curl
RUN python3 -m ensurepip
RUN python3 -m pip install sh

RUN curl -LO https://sourceforge.net/projects/plantuml/files/latest/download
RUN unzip download

ADD ./pumd.py /

ENTRYPOINT ["python3", "pumd.py" ]
