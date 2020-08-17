# Docker commands
# docker run -ti --entrypoint /bin/sh band-site
# docker build .
# docker build . --build-arg UBUNTU_IMAGE=i386/ubuntu:latest <-- for other architectures

# Load ubuntu
ARG UBUNTU_IMAGE=ubuntu:latest

# Load ubuntu
FROM ${UBUNTU_IMAGE}

ENV BUILD_DIR=usr/src/build

RUN mkdir $BUILD_DIR -p

WORKDIR $BUILD_DIR

# copy context over
COPY . .

RUN sed -i 's/\r//g' ./setup.sh

RUN bash ./setup.sh

EXPOSE 6379

CMD ["/home/zdiscord/app/app.sh"] 
