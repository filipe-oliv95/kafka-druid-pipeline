# docker-compose/Dockerfile
FROM apache/druid:30.0.0

USER root

# Cria a pasta da extensão
RUN mkdir -p /opt/druid/extensions/ranger-druid

# Cria a pasta da extensão Ranger-Druid
RUN mkdir -p /opt/druid/extensions/ranger-druid-security

# Copia o código/config da extensão Ranger-Druid
COPY druid-extensions/* /opt/druid/extensions/ranger-druid/

# Copia o plugin Ranger-Druid para a pasta de extensões
COPY ranger-druid-plugin-2.4.0.jar /opt/druid/extensions/ranger-druid-security/

# Copia todos os JARs de dependência (Hadoop + Woodstox/StAX)
COPY hadoop-dependencies/*.jar /opt/druid/extensions/ranger-druid/

# Garante que tudo no diretório da extensão esteja no classpath
ENV DRUID_EXTRA_CLASSPATH="/opt/druid/extensions/ranger-druid/*"

USER druid
