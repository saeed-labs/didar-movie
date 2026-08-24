FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

COPY default.conf /etc/nginx/conf.d/default.conf
COPY upstream.inc /etc/nginx/conf.d/upstream.inc
COPY locations.inc /etc/nginx/conf.d/locations.inc
COPY errors.inc /etc/nginx/conf.d/errors.inc


