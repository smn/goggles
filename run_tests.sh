#!/bin/bash

set -e

find ./goggles -name '*.pyc' -delete
flake8 --exclude=goggles/ui/settings.py,migrations,ve,test_settings.py,local_settings.py .
coverage erase
DJANGO_SETTINGS_MODULE=test_settings py.test goggles "$@"
coverage html
