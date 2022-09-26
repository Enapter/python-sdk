#!/bin/bash

set -e

avahi-daemon --daemonize --no-drop-root

exec "$@"
