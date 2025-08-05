#!/bin/bash
set -xe

./setup.sh
#get start api ranger-admin
sleep 120
cp /opt/ranger_usersync/conf/ranger-ugsync-site.xml /tmp/ranger-ugsync-site.xml
xmlstarlet ed  -u "//property[name='ranger.usersync.enabled']/value"  -v true /tmp/ranger-ugsync-site.xml > /opt/ranger_usersync/conf/ranger-ugsync-site.xml

cp /opt/ranger_usersync/conf/ranger-ugsync-site.xml /tmp/ranger-ugsync-site.xml
xmlstarlet ed  -u "//property[name='ranger.usersync.group.searchenabled']/value"  -v true /tmp/ranger-ugsync-site.xml > /opt/ranger_usersync/conf/ranger-ugsync-site.xml

./ranger-usersync-services.sh start

tail -f /var/log/ranger/usersync/usersync-usersync-*
