#!/bin/sh

set -e

uwsgi --ini=/workdir/uwsgi.ini --http :8000 --listen 64
