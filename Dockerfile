# Dockerfile for building a Docker container.  See https://www.docker.com/
# Install wikimedia runscoring, with dependencies
# See: https://github.com/wikimedia/revscoring

# Build via docker build --rm -t nealmcb/revscoring:0.3 .

FROM jupyter/notebook

RUN DEBIAN_FRONTEND=noninteractive apt-get update && DEBIAN_FRONTEND=noninteractive apt-get upgrade -y

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
  python3-dev \
  python3-numpy \
  python3-scipy \
  g++ \
  gfortran \
  liblapack-dev \
  libopenblas-dev \
  myspell-pt \
  myspell-fa \
  myspell-en-au \
  myspell-en-gb \
  myspell-en-us \
  myspell-en-za \
  myspell-fr \
  myspell-es \
  myspell-he \
  hunspell-vi \
  aspell-id

RUN pip3 install --user revscoring

RUN python3 -m nltk.downloader stopwords
