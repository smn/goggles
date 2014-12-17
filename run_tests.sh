#!/bin/bash

set -e

DJANGO_SETTINGS_MODULE=goggles.ui.settings py.test goggles
