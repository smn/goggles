#!/bin/bash

set -e

find ./goggles -name '*.pyc' -delete
flake8 --exclude=goggles/ui/settings.py,migrations,ve,twisted_django_settings.py,local_settings.py .
coverage erase
DJANGO_SETTINGS_MODULE=twisted_django_settings py.test goggles "$@"
coverage html
