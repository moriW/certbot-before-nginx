FROM nginx:mainline-alpine

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

RUN apk add --update --no-cache python3 py3-pip && \
  ln -sf python3 /usr/bin/python

RUN pip3 config set global.index-url http://mirrors.aliyun.com/pypi/simple && \
  pip3 config set install.trusted-host mirrors.aliyun.com

RUN pip3 install --no-cache-dir certbot --break-system-packages

WORKDIR /app

COPY cert.py .
