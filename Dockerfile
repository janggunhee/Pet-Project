# 어느 이미지를 불러올 것인가
FROM        lanark/pet-base
# 유저 정보
MAINTAINER  dfg1499@gmail.com
# 언어 환경 설정
ENV         LANG C.UTF-8
ENV         DJANGO_SETTINGS_MODULE config.settings.deploy

# 현재 폴더 전체를 /srv/app에 복사
COPY        . /srv/app
# requirements 설치
# base애서 이미 설치했으므로 통과된다,
RUN         /root/.pyenv/versions/app/bin/pip install -r \
            /srv/app/requirements.txt

# pyenv 환경 설정
WORKDIR     /srv/app
RUN         pyenv local app

# Nginx
RUN         cp /srv/app/.config/deploy/nginx/nginx.conf \
                /etc/nginx/nginx.conf
RUN         cp /srv/app/.config/deploy/nginx/app.conf /etc/nginx/sites-available/
RUN         rm -rf /etc/nginx/sites-enabled/*
RUN         ln -sf /etc/nginx/sites-available/app.conf \
                    /etc/nginx/sites-enabled/app.conf

# uWSGI
RUN         mkdir -p /var/log/uwsgi/app

# rabbitMQ install
RUN         apt-get -y update
RUN         apt-get -y install rabbitmq-server

# supervisor
RUN         cp /srv/app/.config/deploy/supervisor/* \
                /etc/supervisor/conf.d/
CMD         supervisord -n

# port open
EXPOSE      80
EXPOSE      5432
