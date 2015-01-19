__author__ = 'Christof Pieloth'

from .installer import Installer
from packbacker.pluginloader import PluginLoader
from packbacker.pluginloader import BaseClassCondition


def installer_prototypes(path):
    """Returns prototypes of all known installers."""
    prototypes = []
    loader = PluginLoader()
    loader.load_directory(path, BaseClassCondition(Installer))
    for k in loader.plugins:
        prototypes.append(loader.plugins[k]().prototype())

    return prototypes
