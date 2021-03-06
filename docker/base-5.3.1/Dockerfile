FROM debian:stretch

# We switched here to debian, as there seems no ZSH 5.3 in ubuntu.

RUN \
  apt update && \
  echo 'golang-go golang-go/dashboard boolean false' | debconf-set-selections && \
  DEBIAN_FRONTEND=noninteractive apt install -y \
  curl \
  git \
  zsh=5.3.1-* \
  mercurial \
  subversion \
  golang \
  jq \
  nodejs \
  ruby \
  python \
  python-virtualenv \
  sudo \
  locales \
  vim

RUN adduser --shell /bin/zsh --gecos 'fred' --disabled-password fred
# Locale generation is different in debian. We need to enable en_US
# locale and then regenerate locales.
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen
RUN locale-gen "en_US.UTF-8"

COPY docker/fred-sudoers /etc/sudoers.d/fred

USER fred
WORKDIR /home/fred
ENV LANG=en_US.UTF-8
ENV TERM=xterm-256color
ENV DEFAULT_USER=fred
ENV P9K_CONTEXT_ALWAYS_SHOW=true

RUN touch .zshrc

CMD ["/bin/zsh", "-l"]
