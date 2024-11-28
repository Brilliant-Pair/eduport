FROM postgres:15-bullseye

COPY ./docker/local/postgres/scripts /usr/local/bin/scripts

RUN chmod +x /usr/local/bin/scripts/*

RUN mv /usr/local/bin/scripts/* /usr/local/bin \
    && rmdir /usr/local/bin/scripts

EXPOSE 5432