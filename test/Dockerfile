FROM debian:jessie

ENV DEBIAN_FRONTEND noninteractive

RUN echo 'Europe/Berlin' > /etc/timezone && dpkg-reconfigure tzdata
RUN echo 'APT::Install-Recommends "0";' > /etc/apt/apt.conf.d/01recommends
RUN apt-get update && apt-get install -yq apt-utils apt-transport-https curl ca-certificates locales bzip2 xz-utils git openssh-client file

RUN apt-get update && \
    apt-get -yq install wget less && \
    apt-get -yq install zsh-common zsh
    #wget "http://ftp.de.debian.org/debian/pool/main/z/zsh/zsh-static_5.2-3_amd64.deb" && \
    #dpkg -i zsh-static_5.2-3_amd64.deb

# We need to regenerate the locale, so that powerlevel9k will work correctly
RUN sed -r 's/^#\s*((en_US|de_DE).UTF-8 UTF-8)/\1/g' -i /etc/locale.gen && locale-gen
RUN update-locale LANG=en_US.UTF-8

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV TERM="xterm-256colors"
