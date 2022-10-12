#!/bin/sh
set -e

apt-get update && apt-get install -y --no-install-recommends avahi-daemon libnss-mdns

# allow hostnames with more labels to be resolved. so that we can
# resolve node1.mycluster.local.
# (https://github.com/lathiat/nss-mdns#etcmdnsallow)
echo '*' > /etc/mdns.allow

# Configure NSSwitch to use the mdns4 plugin so mdns.allow is respected
sed -i "s/hosts:.*/hosts:          files mdns4 dns/g" /etc/nsswitch.conf
printf "[server]\nenable-dbus=no\n" >> /etc/avahi/avahi-daemon.conf
chmod 755 /etc/avahi/avahi-daemon.conf
mkdir -p /var/run/avahi-daemon
chown avahi:avahi /var/run/avahi-daemon
chmod 755 /var/run/avahi-daemon

cat <<EOF > entrypoint.sh
#!/bin/bash

set -e

avahi-daemon --daemonize --no-drop-root

exec "\$@"
EOF
chmod 755 entrypoint.sh
