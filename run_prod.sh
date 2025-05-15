#!/bin/bash
gunicorn video_feed.wsgi:application \
  --env DJANGO_SETTINGS_MODULE=video_feed.settings.prod \
  --bind 0.0.0.0:8000

