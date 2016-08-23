from .base import BaseFilesStorage


def includeme(config):
    BaseFilesStorage.settings = config.registry.settings
