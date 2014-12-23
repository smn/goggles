#!/bin/bash

set -e

find ./goggles -name '*.pyc' -delete
coverage erase
DJANGO_SETTINGS_MODULE=test_settings py.test goggles "$@"
coverage html