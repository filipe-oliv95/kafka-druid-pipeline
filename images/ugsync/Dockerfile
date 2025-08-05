FROM armadik/ranger-builds:2.4.0 as base

FROM ubuntu:22.04

COPY --from=base /opt/ranger /opt/ranger-src

ARG RANGER_VERSION=2.4.0
ENV RANGER_VERSION=${RANGER_VERSION}

RUN apt-get update && \
    apt-get install -y openjdk-8-jdk python3-minimal python-is-python3 vim xmlstarlet && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash ranger

RUN tar -zxf /opt/ranger-src/target/ranger-$RANGER_VERSION-usersync.tar.gz -C /opt/  && \
    ln -s /opt/ranger-$RANGER_VERSION-usersync /opt/ranger_usersync && \
    rm -rf /opt/ranger-src/target/*

ENV JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64

COPY bootstrap.sh /opt/ranger_usersync/
RUN chmod +x /opt/ranger_usersync/bootstrap.sh
RUN chown -R ranger:ranger /opt/
WORKDIR /opt/ranger_usersync/

ENTRYPOINT ["/opt/ranger_usersync/bootstrap.sh"]
ENTRYPOINT ["bash"]