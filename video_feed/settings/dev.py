from .base import *

DEBUG = True
ALLOWED_HOSTS = [host.strip() for host in env("ALLOWED_HOSTS").split(",")]


