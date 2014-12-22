#!/bin/bash

set -e

find ./goggles -name '*.pyc' -delete
coverage erase
DJANGO_SETTINGS_MODULE=goggles.ui.settings py.test goggles "$@"
coverage html